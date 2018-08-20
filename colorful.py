#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:30:25 2018

@author: salbiah
"""
"""
import requests
import cv2
from PIL import Image
import numpy as np
from io import StringIO

def get_image_from_url(imgurl):
    resp = requests.get(imgurl)
    #imgbytes = resp.content
    img = np.array(Image.open(StringIO(resp.content)))
    return img
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

def colorfulness (img):
    image1 = get_image_from_url(img)
    if image1 != 'NaN':
        (B, G, R) = cv2.split(image1.astype("float"))
        rg = np.absolute(R-G)
        yb = np.absolute(0.5*(R+G)-B)
        (rbMean,rbStd) = (np.mean(rg),np.std(rg))
        (ybMean,ybStd) = (np.mean(yb),np.std(yb))
        stdRoot = np.sqrt((rbStd**2)+(ybStd**2))
        meanRoot = np.sqrt((rbMean**2)+(ybMean**2))
        colorful = stdRoot + (0.3*meanRoot)
    else:
        colorful = 'error'
    return colorful

#url = 'https://scontent.xx.fbcdn.net/v/t45.1600-4/s110x80/708196_6007259173086_56048_n.jpg?_nc_cat=0&oh=95c63faf15a815d6f204fd14bd9b3c95&oe=5B899250'
#colorful = colorfulness(url)
#print(colorful)

data='/Users/salbiah/ADA/url_2.csv'

df = pd.read_csv(data)
#print(df)
color = []
for index,row in df.iterrows():
    #print (row['latitude'],row['longitude'])
    value = colorfulness(row['_c0'])
    color.append(value)
    print(index)
        
df['colorful'] = color   
