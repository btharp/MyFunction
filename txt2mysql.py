#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Coded by BT

import pandas as pd
import pymysql
from sqlalchemy import create_engine
import os


#读取数据库
#初始化数据库
db_info = {'user': 'root', 'password': 'Peng%Mai_zhf@2014','host': '121.199.15.106','port': 3306,'database': 'dc_WeChat'}
engine = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=utf8' % db_info, encoding='utf-8',connect_args={'charset':'utf8'})


for root,dirs,files in os.walk("E:\data"):
    print(root)
    print(dirs)
    print(files)

for i in range(len(files)):
    df=pd.read_csv('E:/data/'+files[i],sep='\t',index_col=False,error_bad_lines=False)
    pd.io.sql.to_sql(df,files[i].replace(".txt",""),con=engine, index=False, if_exists='replace')