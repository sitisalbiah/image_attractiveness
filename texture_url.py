#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 16:37:36 2018

@author: salbiah
"""

import numpy as np
from urllib.request import Request,urlopen
#from urllib.parse import unquote
#from difflib import *
import urllib.error
import cv2
import pandas as pd
import socket
import http
import skimage
from skimage.io import imread
from skimage.feature import greycomatrix
from skimage.feature import greycoprops

def get_image_from_url(url):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers ={'User-Agent':user_agent,}
    #resp = urlopen(url)
    request = Request(url,None,headers)
    try:
        response = urlopen(request)
        image = np.asarray(bytearray(response.read()),dtype="uint8")        
        image = cv2.imdecode(image,cv2.IMREAD_COLOR)  
    except urllib.error.HTTPError as e: 
        image = 'NaN'
    except urllib.error.URLError as e:
        #image = e.read().decode("utf8", 'ignore')
        image = 'NaN'
    except socket.error as e: 
        image = 'NaN'
    except socket.timeout as e: 
        image = 'NaN'
    except UnicodeEncodeError as e: 
        image = 'NaN'
    except http.client.BadStatusLine as e: 
        image = 'NaN'
    except http.client.IncompleteRead as e: 
        image = 'NaN'   
        
    return image

def texture (img):
    image1 = get_image_from_url(img)
    if image1 != 'NaN':
        #im = skimage.img_as_ubyte(image1)
        im = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        g = skimage.feature.greycomatrix(im, [1], [0], 256, symmetric=True, normed=True)

        tex_cont= greycoprops(g, 'contrast')[0][0]
        tex_energy= greycoprops(g, 'energy')[0][0]
        tex_homogeneity= greycoprops(g, 'homogeneity')[0][0]
        tex_correlation=greycoprops(g, 'correlation')[0][0]
        tex_dissimilarity=greycoprops(g, 'dissimilarity')[0][0]
        tex_ASM=greycoprops(g, 'ASM')[0][0]     
    else:
        tex_cont = 'error'
        tex_energy = 'error'
        tex_homogeneity = 'error'
        tex_correlation = 'error' 
        tex_dissimilarity = 'error' 
        tex_ASM = 'error' 
        
    return tex_cont,tex_energy,tex_homogeneity,tex_correlation,tex_dissimilarity,tex_ASM    

data='/Users/salbiah/ADA/coding-Image-features-set/image_tagging/color_bright_saturation.csv'

df = pd.read_csv(data)
#print(df)
tex_cont = []
tex_energy = []
tex_homogeneity = []
tex_correlation = []
tex_dissimilarity = []
tex_ASM   = []

for index,row in df.iterrows():
    #print (row['latitude'],row['longitude'])
    value1,value2,value3,value4,value5,value6 = texture(row['_c0'])
    tex_cont.append(value1)
    tex_energy.append(value2)
    tex_homogeneity.append(value3)
    tex_correlation.append(value4)
    tex_dissimilarity.append(value5)
    tex_ASM.append(value6)
    print(index)
        
df['tex_cobtrast'] = tex_cont
df['tex_energy'] = tex_energy
df['tex_homogeneity'] = tex_homogeneity
df['tex_correlation '] = tex_correlation  
df['tex_dissimilarity'] = tex_dissimilarity 
df['tex_ASM'] = tex_ASM  