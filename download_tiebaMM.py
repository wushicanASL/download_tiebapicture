#coding:utf-8
import urllib.request
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import os
import re
import time

#获取html
def getUrl(url):
    try:
        time.sleep(2)
        req = urllib.request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')
        response = urllib.request.urlopen(req)
        html = response.read()
    except HTTPError as e:
        return None
    except ConnectionResetError as e:
        return None
    return html

#获取beautifulSoup对象
def getBSoj(url):
    try:
        html=getUrl(url)
        bsoj = BeautifulSoup(html,"html.parser")
    except AttributeError as e:
        return None
    return bsoj

def getTitle(url):
    return getBSoj(url).body.h1

#获取一个页面所有图片的URL
def getImg(url):
    
    bsoj=getBSoj(url)
    namelist= bsoj.findAll("img",{'class':'BDE_Image'})
    length = len(namelist)
    print(length)
    #保存图片
    for i in range(length):
        saveimg(namelist[i].get('src'))
    return None

#将图片保存到磁盘
def saveimg(url):
    url = str(url)
    filename = url.split('/')[-1]  #以最后一个/后的字符串作为图片文件名
    try:
        with open(filename,'wb') as f:  #以二进制保存图片
            img = getUrl(url)
            print("saving picture ....%s"%filename)
            f.write(img)
    except HTTPError as e:
        print(e)
    except FileNotFoundError as e1:
        print(e1)
    except OSError as e2:
        print(e2)

#获取整个帖子的有多少页
def get_pagenum(url):
    bsoj=getBSoj(url)
    pages=bsoj.findAll('span',{'class':"red"})
    num=pages[-1].text
    return num

    
if __name__ == '__main__':
    folder='MM2'
    if not os.path.isdir(folder): 
        os.mkdir(folder)
    os.chdir(folder)
    
    url4='http://tieba.baidu.com/p/4139224563'
    num=int(get_pagenum(url4))
    
    for i in range(num):
        url5=url4+'?pn='+str(i)
        getImg(url5)
    print("已下载完成")
