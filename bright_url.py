#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 17:13:22 2018

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

def brightness (img):
    image1 = get_image_from_url(img)
    if image1 != 'NaN':
        imgYUV = cv2.cvtColor(image1,cv2.COLOR_BGR2YUV)
        Y,U,V = cv2.split(imgYUV)
        Y_average = np.average(Y)
        Y_SD = np.std(Y)
        Y_max = np.amax(Y)
        Y_min = np.amin(Y)
    else:
        Y_average = 'error'
        Y_SD = 'error'
        Y_max = 'error'
        Y_min = 'error'
    return Y_average,Y_SD,Y_max,Y_min

data='/Users/salbiah/ADA/coding-Image-features-set/image_tagging/color.csv'

df = pd.read_csv(data)
#print(df)
bright_av = []
bright_sd = []
bright_max = []
bright_min = []
for index,row in df.iterrows():
    #print (row['latitude'],row['longitude'])
    value1,value2,value3,value4 = brightness(row['_c0'])
    bright_av.append(value1)
    bright_sd.append(value2)
    bright_max.append(value3)
    bright_min.append(value4)
    print(index)
        
df['bright_avg'] = bright_av
df['bright_sd'] = bright_sd
df['bright_max'] = bright_max
df['bright_min'] = bright_min  

    