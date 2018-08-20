#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 11:26:03 2018

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

def saturation (img):
    image1 = get_image_from_url(img)
    if image1 != 'NaN':
        imgHLS = cv2.cvtColor(image1,cv2.COLOR_BGR2HLS)
        H,L,S = cv2.split(imgHLS)
        S_average = np.average(S)
        S_SD = np.std(S)
        S_max = np.amax(S)
        S_min = np.amin(S)
    else:
        S_average = 'error'
        S_SD = 'error'
        S_max = 'error'
        S_min = 'error'
    return S_average,S_SD,S_max,S_min

data='/Users/salbiah/ADA/coding-Image-features-set/image_tagging/color_bright.csv'

df = pd.read_csv(data)
#print(df)
saturation_av = []
saturation_sd = []
saturation_max = []
saturation_min = []
for index,row in df.iterrows():
    #print (row['latitude'],row['longitude'])
    value1,value2,value3,value4 = saturation(row['_c0'])
    saturation_av.append(value1)
    saturation_sd.append(value2)
    saturation_max.append(value3)
    saturation_min.append(value4)
    print(index)
        
df['saturation_avg'] = saturation_av
df['saturation_sd'] = saturation_sd
df['saturation_max'] = saturation_max
df['bsaturation_min'] = saturation_min 