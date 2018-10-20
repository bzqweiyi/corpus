# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 13:17:26 2018

@author: User
"""

import jieba
import xlrd




tags=jieba.analyse.extract_tags(text, topK=10)
#print(" ".join(tags))


'''
加载停用词表
'''
def createstoplist(stoppath):
    print('load stopwords...')
    stoplist=[line.strip() for line in codecs.open(stoppath,'r',encoding='utf-8').readlines()]
    stopwords={}.fromkeys(stoplist)
    return stopwords

def tans():
      with codecs.open('C:\pythonSpace\text','w','utf-8') as wopen:
        print('开始...'+wopen)
        with codecs.open('E:\wiki-utf8.txt','r','utf-8') as ropen:
            while True:
                line=ropen.readline().strip()
                i+=1
                print('line '+str(i))
                text=''
                for char in line.split():
                    if isAlpha(char):
                        continue
                    char=cc.convert(char)
                    text+=char
                words=jieba.cut(text)
                seg=''
                for word in words:
                    if word not in stopwords:
                        if len(word)>1 and isAlpha(word)==False: #去掉长度小于1的词和英文
                            if word !='\t':
                                seg+=word+' '
                wopen.write(seg+'\n')
                print('结束!')
                
stopwords=createstoplist('C:\pythonSpace\stoplist.txt')

from datetime import date,datetime



def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))

def excel_table_byname(file,by_name):#修改自己路径
     data = open_excel(file)
     table = data.sheet_by_name(by_name)#获得表格
     nrows = table.nrows  # 拿到总共行
     colnames = table.row_values(0)  # 
     text=''
     for rownum in range(0, nrows): #也就是从Excel第二行开始，第一行表头不算
         row = table.row_values(rownum)         
         text+=(''.join(row))+' '   
     #print(text)          
     return text
 
def main():
    jieba.set_dictionary(r"C:\中医知识收集\分词词典库\jieba.dict.txt.big")

#%% 挂载额外的词库

    dict_path = r"C:\\中医知识收集\\医学\\"
    files = os.listdir(dict_path)
    for file in files:
        jieba.load_userdict(dict_path+file)
    jieba.initialize()
    file=u'C:\\爬虫数据\\后6种慢病-数据爬取整理\\痛风.xls'
    by_name='痛风'
    tables = excel_table_byname(file,by_name)
    jieba.add_word("痛风")
    words=jieba.cut(tables)
    seg=''
    patterns=[]
    stopwords=createstoplist('C:\pythonSpace\stoplist.txt')
    for word in words:
        if word not in stopwords:
            if len(word)>1 and isAlpha(word)==False: #去掉长度小于1的词和英文
                if word not in patterns:
                    patterns.append(word)
                    seg+=word+"\n"
    print(len(seg.split("\n")))               
    file=open('C:\\爬虫数据\\后6种慢病-数据爬取整理\\痛风.txt','w')
    file.write(str(seg));  
    file.close()

if __name__ =="__main__":
    main()