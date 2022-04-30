# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 15:15:20 2022

@author: Eric Buehler
"""

from flask import Flask, request, jsonify, send_file
from PIL import Image

import torch
import torch.nn as nn
from torchvision import datasets, transforms, models

import matplotlib.pyplot as plt
from torch.nn.modules.dropout import Dropout2d

import time

import base64
import io

to_pil = transforms.ToPILImage()

im_resy=80
im_resx=160
nclasses=5
numchannel=3
device=torch.device('cpu')
class network(nn.Module):
    def __init__(self,nclasses):
        super(network, self).__init__()
        self.queries_dim_=256
        latent_dim_=784
        logits_dim= nclasses
        embed_dim=128
        embed_dim_min=16
        dim=3
        self.embed_dim_=embed_dim

        self.convert_up = nn.Sequential( #numchannel -> embed_dim
            nn.Linear(  numchannel, 4),
            nn.Linear(  4, 8),
            nn.Linear(  8, 16),
            nn.Linear(  16, 32),
            nn.Linear(  32, 48),
            nn.Linear(  48, embed_dim)
        )

        self.encoders=[]
        embed_dim_=embed_dim
        while embed_dim_>embed_dim_min:
            layer=nn.Conv2d(in_channels=embed_dim_, out_channels=int(embed_dim_/2), kernel_size=3, stride=1, padding=1).to(device)
            self.encoders.append(layer)
            embed_dim_=int(embed_dim_/2)

        self.decoders=[]
        embed_dim_=embed_dim_min
        while embed_dim_<embed_dim:
            layer=nn.Conv2d(in_channels=embed_dim_, out_channels=int(embed_dim_*2), kernel_size=3, stride=1, padding=1).to(device)
            self.decoders.append(layer)
            embed_dim_=int(embed_dim_*2)
            
        self.convs=[]
        for item in self.encoders:
            self.convs.append(item)
        self.convs.append(nn.BatchNorm2d(embed_dim_min))
        for item in self.decoders:
            self.convs.append(item)
        self.convs.append(nn.BatchNorm2d(embed_dim))
        self.convs=nn.ModuleList(self.convs)

        self.query_gen = nn.Sequential( # embed_dim*4 -> self.queries_dim_
            nn.Linear(  embed_dim*4, 384),
            nn.Linear(  384, 512),
            nn.Linear(  512, 640),
            nn.Linear(  640, 784),
            nn.Linear(  784, 1024),
            nn.Linear(  1024, 784),
            nn.Linear(  784, 640),
            nn.Linear(  640, 512),
            nn.Linear(  512, self.queries_dim_),
        )
        
        self.convert_down = nn.Sequential( #im_resx*im_resy -> 1
            nn.Linear(  im_resx*im_resy, 2048),
            nn.Linear(  2048, 1024),
            nn.Linear(  1024, 784),
            nn.Linear(  784, 512),
            nn.Linear(  512, 256),
            nn.Linear(  256, 128),
            nn.Linear(  128, 1),
        )

        self.pos_emb_x = nn.Embedding(im_resy, embed_dim*1)
        self.pos_emb_y = nn.Embedding(im_resx, embed_dim*1)

        self.pos_matrix_i = torch.zeros (im_resx, im_resy, dtype=torch.long)
        self.pos_matrix_j = torch.zeros (im_resx, im_resy,dtype=torch.long)
        for i in range(im_resy):
            for j in range(im_resx):
                self.pos_matrix_i [j,i]=i
                self.pos_matrix_j [j,i]=j
                       
        self.pos_matrix_j =torch.flatten(self.pos_matrix_j , start_dim=0, end_dim=1) 
        self.pos_matrix_i =torch.flatten(self.pos_matrix_i , start_dim=0, end_dim=1)  

        self.model = PerceiverIO(
            dim = embed_dim*4,                    # dimension of sequence to be encoded
            queries_dim = self.queries_dim_,            # dimension of decoder queries
            logits_dim = nclasses,            # dimension of final logits
            depth = 12,                   # depth of net
            num_latents = 512,           # number of latents, or induced set points, or centroids. different papers giving it different names
            latent_dim = latent_dim_,            # latent dimension
            cross_heads = 1,             # number of heads for cross attention. paper said 1
            latent_heads = 8,            # number of heads for latent self attention, 8
            cross_dim_head = 64,         # number of dimensions per cross attention head
            latent_dim_head = 64,        # number of dimensions per latent self attention head
            weight_tie_layers = False,    # whether to weight tie layers (optional, as indicated in the diagram)
            decoder_ff=True
        ).to(device)

        self.softmax=nn.Softmax(dim=-1)

    def forward(self, x):
        x=torch.permute(x,(0,2,3,1))
        x=self.convert_up(x)
        x=torch.permute(x,(0,3,1,2))
        x_=x.clone() 
        x=torch.flatten(x, start_dim=2, end_dim=3) 

        for layer in self.convs:
            x_=layer(x_)
        x_=torch.flatten(x_, start_dim=2, end_dim=3) 

        x_=torch.permute(x_, (0,2,1)  )
        x=torch.permute(x, (0,2,1)  )

        x=torch.cat([x,x_],dim=2)
        
        pos_matrix_j_=self.pos_matrix_j.repeat(x.shape[0], 1, 1).to(device=device) 
        pos_matrix_i_=self.pos_matrix_i.repeat(x.shape[0], 1, 1).to(device=device) 
        

        pos_emb_y = self.pos_emb_y(pos_matrix_j_)
        pos_emb_y = torch.squeeze(pos_emb_y, 1)
        pos_emb_x = self.pos_emb_x( pos_matrix_i_)
        pos_emb_x = torch.squeeze(pos_emb_x, 1)

        catlist=[x,pos_emb_y,pos_emb_x]
        #print(x.shape,pos_emb_y.shape,pos_emb_x.shape)

        inputs= torch.cat(catlist, 2)
        queries=self.query_gen(inputs)
        outputs=self.model(inputs,queries=queries )

        outputs=torch.permute(outputs, (0,2,1)  )
        outputs=self.convert_down(outputs)
        outputs=torch.permute(outputs, (0,2,1)  )
        outputs=outputs.squeeze_()
        outputs=self.softmax(outputs)
        return outputs
    
class runmodel:
    def __init__(self):
        self.im_resy=80
        self.im_resx=160
        self.nclasses=5
        self.numchannel=3
        self.device=torch.device('cpu')
        self.model=torch.load("model_final.pth", map_location=self.device)
        self.model.eval()
        
        self.transforms = transforms.Compose([
                                     transforms.Resize((80,160)),
                                       transforms.ToTensor()
                                       ])
        
        self.mapping={0:"stop",1:"left",2:"right",3:"forward",4:"backward"}
        
    def __call__(self, image):
        inputs=self.transforms(image).unsqueeze_(0)
        outputs=self.model(inputs.to(self.device))
        outputs_=int(outputs.argmax(-1).cpu().detach())
        output_final=self.mapping[outputs_]
        return output_final
        
        
        

app = Flask(__name__)
model=runmodel()

number=0
pred=None
recenttime=None


@app.route("/im_size", methods=["POST"])
def process_image():
    file = request.files['image']
    # Read the image via file.stream
    img = Image.open(file.stream)

    return jsonify({'size': [img.width, img.height]})

@app.route("/predict", methods=["POST"])
def predict_image():
    global number
    global pred
    global recenttime
    
    timestart=time.time()
    file = request.files['image']
    # Read the image via file.stream
    img = Image.open(file.stream)
    out=model(img)
    timeend=time.time()
    
    number+=1
    pred=out
    recenttime=round(timeend-timestart,2)
    
    return jsonify({'pred':out, 'time_s':timeend-timestart})


@app.route("/")
def index():
    global number
    global pred
    global recenttime
    
    if pred==None:
        return f"""
        <h1>Neuron Control Server</h1>
        <h2>Eric Buehler 2022</h2>
        <h3>Server has started and no predictions have been made.</h3>
        """

    return f"""
    <html>
    <head>
    
    <h1>Neuron Control Server</h1>
    <h2>Eric Buehler 2022</h2>
    <br>
    <h3>{number} predictions have been made since server reset.</h3>
    <h3>Most recent prediction is {pred!r}.</h3>
    <h3>Most recent prediction took {recenttime} seconds.</h3>
    
    </head>
    </html>
    """

if __name__ == "__main__":
    print("Starting server. 192.168.1.157:8000")
    from waitress import serve
    serve(app, host="0.0.0.0", port=8000)
    