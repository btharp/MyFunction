#%%
# -*- coding:utf-8 -*-
import pandas as pd 
import numpy as np 
import os 
from PIL import Image,ImageDraw,ImageFile 
import pytesseract
import cv2 
import imagehash
import collections 


# %%
path='G:/Project/test'
files=os.listdir(path) #文件名列表


'''
s=[]
for i in range(len(files)):
    with open(path+'/'+files[i],'rb') as fb:
        hash=imagehash.average_hash(Image.open(fb))
    s.append(hash)

H=Image.open(path+'/image4.emf')
H2=Image.open(path+'/image1 (2).jpeg')

# 读取图
d={}
for i in range(len(files)):
    try:
        H=Image.open(path+'/'+files[i]).convert('L')
    except ZeroDivisionError:
        pass 
    else:
        img=np.array(H)
        d[files[i]]=img

#  判断是否重复
func = lambda z: dict([(x, y) for y, x in z.items()])
new=func(func(d))
len(new)
'''

# %% 读取图片
d={}
for i in range(len(files)):
    try:
        H=cv2.imread(path+'/'+files[i])
    except ZeroDivisionError:
        pass 
    else:
        try:
            H.shape
        except AttributeError:
            pass
        else:
            d[files[i]]=H

#%% 找出多余的图片
k=list(d.keys())
dup=[]
for i in range(len(d)):
    for j in range(i+1,len(d)):
        if d[k[i]].shape==d[k[j]].shape:
            difference = cv2.subtract(d[k[i]], d[k[j]])
            b, g, r = cv2.split(difference)
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                dup.append(j)

#%% 删除多余的图片
for i in range(len(dup)):
    try:
        os.remove(path+'/'+k[dup[i]])
    except FileNotFoundError:
        pass
    continue 
# %%
