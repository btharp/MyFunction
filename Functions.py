#%% import libraries
import openpyxl
from openpyxl_image_loader import SheetImageLoader
import pandas as pd 
import tkinter as tk
from tkinter import filedialog
import shutil
import os
import pymssql
import pymysql
from sqlalchemy import create_engine
import pyodbc
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process
from dateutil.parser import parse
import datetime



#%% 
def get_file_path():
    '''
    打开文件对话框，获取文件路径、名称、后缀
    '''
    root = tk.Tk()
    root.wm_attributes('-topmost',1) # 弹窗置顶
    root.withdraw()

    file_path = filedialog.askopenfilename() 
    path, file_name = os.path.split(file_path)
    file_name_root,ext=os.path.splitext(file_name)

    return path,file_path,file_name,file_name_root,ext 



def isfloat(str):
    '''
    用于判断是否为空，如DataFrame的某个列名
    '''
    try:
        float(str)
        return True
    except ValueError:
        return False



def find_row(num_value,demo_df):
    """
    获取excel特定值所在单元格的行
    """
    for indexs in demo_df.index:
        for i in range(len(demo_df.loc[indexs].values)):
            if (str(demo_df.loc[indexs].values[i]) == num_value):
                row = str(indexs+2).rstrip('L')
                return row



def change_Num_ToChar(s):
    '''
    把数字转换成相应的字母字符,1-->'A' 27-->'AA'
    '''
    a = [chr(i) for i in range(65, 91)]
    ss = ''
    b = []
    if s <= 26:
        b = [s]
    else:
        while s > 26:
            c = s // 26  # 商
            d = s % 26  # 余数
            b = b + [d]
            s = c
        b = b + [s]
    b.reverse()
    for i in b:
        ss = ss + a[i - 1]
    return ss



def read_excel(file_path,sheet_name,first_value,last_value):
    '''
    从excel中读取dataframe, 假定首尾几行内容不想关，需要去除
    first_value是A列真正起始行的特定内容
    last_value是A列真正结束行下一行的特定内容
    '''
    f=open(file_path,'rb')

    df=pd.read_excel(f,header=None,sheet_name=sheet_name)
    
    # 获取起止行号
    row_num_start = int(find_row(first_value,df))-2 # 初始行号
    row_num_end =int(find_row(last_value,df))-2 # 结尾行号

    # 删除头尾几行
    lastDown=len(df)
    df=df.drop(df.index[row_num_end:lastDown]) 
    df = df.drop(df.index[0:row_num_start])

    # 重新改列名
    new_header = df.iloc[0] 
    df = df[1:] 
    df.columns = new_header
    df.reset_index(drop=True,inplace=True) #重置index

    f.close()
    return df,row_num_start,row_num_end



def save_img_excel(file_path,sheet_name,first_value,last_value,name_col,save_path):
    '''
    从excel中提取某列的图片，并按照另一列对应值重命名
    要求excel为xlsx
    '''
    df,row_num_start,row_num_end=read_excel(file_path,sheet_name,first_value,last_value)
    # 获取图片列号
    columns=list(df.columns)
    col_num=change_Num_ToChar(columns.index(name_col)+1)

    # 读取及复制图片
    #loading the Excel File and the sheet
    pxl_doc = openpyxl.load_workbook(file_path)
    sheet = pxl_doc[sheet_name]
    # calling the image_loader
    image_loader = SheetImageLoader(sheet)


    # 复制图片
    ls=range((row_num_start+2),(row_num_end)+1) # 图片行号的list
    for i in range(len(ls)):
        #get the image (put the cell you need instead of 'A1')
        try:
            image = image_loader.get(col_num+str(ls[i])) # 获取图片
            try:
                image_name=name_col[i] # 命名图片
                if image.mode=='RGBA':
                    image.save(save_path+image_name+'.png') # 保存图片
                else:
                    image.convert('RGB')
                    image.save(save_path+image_name+'.jpg') # 保存图片
            except:
                pass
        except:
            pass




def df_to_sql(df,user,password,host,port,database,table,if_exists,sql_type):
    '''
    将df导入mysql或者mssql，if_exists选择append或replace
    '''
    db_info = {'user': user, 'password': password,'host': host,'port': int(port),'database': database}
    if sql_type=="mssql":
        engine = create_engine('mssql+pymssql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=utf8' % db_info, encoding='utf-8',connect_args={'charset':'utf8'})
    elif sql_type=="mysql":
        engine = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=utf8' % db_info, encoding='utf-8',connect_args={'charset':'utf8'})
    df.to_sql(table,engine,if_exists=if_exists, index=False)



# %%
def fuzzy_match(df1,df2,list1,list2,Original,ToMatch):
    '''

    '''
    list_match={}
    for i in range(len(list1)):
        
        match=process.extractOne(list1[i].replace(" ",""),list2,scorer=fuzz.token_sort_ratio)
        list_match.update({list1[i]:match})


    Match=pd.DataFrame(list_match).T.reset_index()
    Match.columns=[Original,ToMatch,"匹配率","index"]
    dfjoin=pd.merge(df1,Match,how="left",on=[Original])
    dfjoin.drop([ToMatch],axis=1,inplace=True)
    dfjoin2=pd.merge(dfjoin,df2,how="left",on=["index"])
    dfjoin2.drop(["index"],axis=1,inplace=True)

    with pd.ExcelWriter(r"匹配表.xlsx") as xlsx:   # 生成匹配表
        Match.to_excel(xlsx,sheet_name="匹配关系表",index=False)
        dfjoin2.to_excel(xlsx,sheet_name="匹配数据",index=False)




# class Finance():
import tushare as ts
import pandas as pd
import pymysql
import pymssql
from sqlalchemy import create_engine
import os


ts.set_token('632210e8afbd5a1fc1634b019b27df3866dcb8ce7035d7a9d2e39117')  #设置token
pro = ts.pro_api()  # 初始化


def get_fina(StockList,start_date,end_date,filename):
    '''
    调取财务指标
    #创建空白dataframe
    '''
    fina=pro.fina_indicator(ts_code="000000")
    #日期的格式为"20190631"
    #调取数据
    for i in range(len(StockList)):
        df=pro.fina_indicator(ts_code=StockList[i],start_date=start_date,end_date=end_date)
        fina=fina.append(df)
    #写入excel
    fina.to_excel(filename)
    #写入mysql
    # pd.io.sql.to_sql(fina,"Indicators",con=engine, index=False, if_exists='append')
    return fina

 
def get_monthly(StockList,start_date,end_date,filename):
    '''
    调取月线数据
    filename为存储路径和文件名，如："X:/02专题分析/上市公司/上市公司月线.xlsx"
    '''
    pe=pro.monthly(ts_code="000000")
    for i in range(len(StockList)):    
        de=pro.monthly(ts_code=StockList[i],start_date=start_date,end_date=end_date)
        pe=pe.append(de)
    #写入excel
    pe.to_excel(filename)
    #写入mysql
    # pd.io.sql.to_sql(pe,"Monthly",con=engine, index=False, if_exists='append')
    return pe

 
def get_daily(StockList,start_date,end_date,filename):
    ''''
    调取日线数据 filename为存储路径和文件名，如："X:/02专题分析/上市公司/上市公司日线.xlsx"
    '''
    pe=pro.daily(ts_code="000000")
    for i in range(len(StockList)):    
        de=pro.daily(ts_code=StockList[i],start_date=start_date,end_date=end_date)
        pe=pe.append(de)
    #写入excel
    pe.to_excel(filename)
    #写入mysql
    # pd.io.sql.to_sql(pe,"Daily",con=engine, index=False, if_exists='append')
    return pe