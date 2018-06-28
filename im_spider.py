# -*- coding: UTF-8 -*-
import urllib
import re
import requests
import random
import json
import sys
import os

reload(sys)

sys.setdefaultencoding('utf-8')

def user_agent():
    #反爬虫
    user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", 
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",  
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",  
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",  
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",  
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", 
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", 
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", 
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",  
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",  
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"  
           ]
    user_agent = random.choice(user_agent_list)
    return user_agent


def load_page(url):
    headers = {}
    headers['User-Agent'] = user_agent()
    #requests.add_header("Host", "image.baidu.com")
    res = requests.get(url, headers=headers,timeout=30)
    res.encoding = 'utf-8'
    html = res.text
    return html

def find_url(html):
    '''正则查找objurl'''
    with open("js.txt", "w") as f:
        f.write(html)    
    pattern = re.compile('"objURL":"(.*?)"', re.S)
    context = pattern.findall(html)
    return context

def  baidtu_uncomplie(url):
    '''objurl解码'''
    res = ''
    c = ['_z2C$q', '_z&e3B', 'AzdH3F']
    d= {'w':'a', 'k':'b', 'v':'c', '1':'d', 'j':'e', 'u':'f', '2':'g', 'i':'h', 't':'i', '3':'j', 'h':'k', 's':'l', '4':'m', 'g':'n', '5':'o', 'r':'p', 'q':'q', '6':'r', 'f':'s', 'p':'t', '7':'u', 'e':'v', 'o':'w', '8':'1', 'd':'2', 'n':'3', '9':'4', 'c':'5', 'm':'6', '0':'7', 'b':'8', 'l':'9', 'a':'0', '_z2C$q':':', '_z&e3B':'.', 'AzdH3F':'/'}
    if(url==None or 'http' in url):
        return url
    else:
        j= url
        for m in c:
            j=j.replace(m,d[m])
        for char in j:
            if re.match('^[a-w\d]+$',char):
                char = d[char]
            res= res+char
        return res



def main():
    key_word = raw_input("爬取关键字")
    num = raw_input("爬取数量(30倍数)")
    i = 0
    img_url = []
    #print(num)

    #获取图片链接
    while (int(i) <= (int(num) - 30)):
        url = "http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&fp=result&word="+ key_word +"&pn="+ str(i) +"&rn=30"
        #print(url)
        html = str(load_page(url))
        #print (json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': ')))
        #with open("js.txt", "w") as f:
        #    f.write(json_data)
        #deal_json(json_data)
        #print(html)
        context = find_url(html)
        for x in context:
            res = baidtu_uncomplie(x)
            img_url.append(res)
        i = i+30
        #print(i)
    cur_path = os.path.abspath(os.curdir)
    goal_path = cur_path + '/image'
    #print(goal_path)
    #print(os.path.exists(goal_path))
    if  not os.path.exists(goal_path):
        os.mkdir('image')
    j = 0
    dic = [".jpg",".png",".JPEG",".jpeg",".JPG",".PNG",".bmp",".BMP"]
    for x in img_url:
        file_type = x[x.rfind('.'):]
        if not file_type in dic:
            continue
        loc = goal_path +'/'+str(j) +file_type
        #print(x)
        #print(loc)
        #urllib.urlretrieve(x,loc)

        headers = {}
        headers['User-Agent'] = user_agent()
        #requests.add_header("Host", "image.baidu.com")
        try:
            res = requests.get(x, headers=headers,timeout=5)
        except Exception as e:
            print(e)
            print(x)
            continue
        else:
            res.encoding = 'utf-8'
            html = res.content
            print("正在下载第%s张"%j)
            with open(loc, "w") as f:
                f.write(html)
            j += 1

 	    

        #print(file_type)
        #img = load_page(x)




if __name__ == '__main__':
    main()