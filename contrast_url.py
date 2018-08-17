#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 14:50:42 2018

@author: salbiah
"""

import numpy as np
from urllib.request import Request,urlopen
#from urllib.parse import unquote
#from difflib import *
import urllib.error
import cv2
import math
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

def contrast (img):
    image1 = get_image_from_url(img)
    if image1 != 'NaN':
        cont = 0.0
        resolutions = [1, 2, 4, 8, 16, 25, 50, 100, 200]
        rIm = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        h0, w0 = rIm.shape[:2]
        for i in range(len(resolutions)):
            if i > 0:
                div = resolutions[i]
                rIm = cv2.resize(rIm,(int(w0/div),int(h0/div)))                
            (H,W) = np.shape(rIm)
            l = np.divide(rIm,255) * 2.2

            rL = 100 * np.sqrt(l)

            lc = 0.0
            c = []
            w = []
            LC = []
            for x in range(H-1):
                for y in range (W-1):
                    if x == 1:
                        if y ==1:
                            lc = lc + (abs(rL[x,y] - rL[x,y+1]) + abs (rL[x,y] - rL[x+1,y])) /2
                        elif y == W:
                            lc = lc + (abs(rL[x,y] - rL[x,y-1]) + abs (rL[x,y] - rL[x+1,y])) /2
                        else:
                            lc = lc + (abs(rL[x,y] - rL[x,y-1]) + abs (rL[x,y] - rL[x,y+1]) + abs(rL[x,y] - rL[x+1,y])) /3
                    elif x == H:
                        if y == 1:
                            lc = lc + (abs(rL[x,y] - rL[x,y+1]) + abs (rL[x,y] - rL[x-1,y])) /2
                        elif y == W:
                            lc = lc + (abs(rL[x,y] - rL[x,y-1]) + abs(rL[x, y] - rL[x-1,y])) / 2
                        else:
                            lc = lc + (abs(rL[x,y] - rL[x,y - 1]) + abs(rL[x,y] - rL[x,y+1]) + abs(rL[x,y] - rL[x-1,y])) / 3

                    else:
                        lc = lc + (abs(rL[x, y] - rL[x, y-1]) + abs(rL[x, y] - rL[x, y+1]) + abs(rL[x,y] - rL[x-1, y]) + abs(rL[x,y] - rL[x+1,y])) / 4

            temp = lc/(W*H)
            c.append(temp)
            temp2 = (-0.406385*(i/9)+0.334573)*(i/9)+0.0877526
            w.append(temp2)

            temp3 = temp*temp2
            LC.append(temp3)
            cont = cont + temp3
    else:
        cont = 'error'
    return cont

data='/Users/salbiah/ADA/coding-Image-features-set/image_tagging/color_bright_saturation.csv'

df = pd.read_csv(data)
#print(df)
contra = []

for index,row in df.iterrows():
    #print (row['latitude'],row['longitude'])
    value = contrast(row['_c0'])
    contra.append(value)
    print(index)
        
df['contrast'] = contra
