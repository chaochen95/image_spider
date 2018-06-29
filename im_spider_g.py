# -*- coding: UTF-8 -*-
import urllib
import re
import requests
import random
import json
import sys
import os
from PIL import Image
import io

reload(sys)
sys.setdefaultencoding('utf-8')

'''
template = [
https://www.googleapis.com/customsearch/v1?
q={searchTerms} #请求内容
&num={count?}   #每页显示数量 0-10
&start={startIndex?}#起始页码
&lr={language?} #Restricts the search to documents written in a particular language 
&safe={safe?}   #安全搜索 high: Enables highest level of SafeSearch filtering. medium: Enables moderate SafeSearch filtering off: Disables SafeSearch filtering. (default)
&cx={cx?}#custom search engine ID
&sort={sort?}#
&filter={filter?} #duplicate content filter 1:on 0:off
&gl={gl?}
&cr={cr?}
&googlehost={googleHost?}
&c2coff={disableCnTwTranslation?}   #Turns off the translation between zh-CN and zh-TW
&hq={hq?}
&hl={hl?}
&siteSearch={siteSearch?}   #Specifies all search results should be pages from a given site.
&siteSearchFilter={siteSearchFilter?}   #Controls whether to include or exclude results from the site named in the siteSearch parameter. "e": exclude "i": include
&exactTerms={exactTerms?}   #Identifies a phrase that all documents in the search results must contain
&excludeTerms={excludeTerms?}   #Identifies a word or phrase that should not appear in any documents in the search results
&linkSite={linkSite?}   #Specifies that all search results should contain a link to a particular URL
&orTerms={orTerms?} #Provides additional search terms to check for in a document, where each document in the search results must contain at least one of the additional search terms.
&relatedSite={relatedSite?} #Specifies that all search results should be pages that are related to the specified URL.
&dateRestrict={dateRestrict?}   #按时间查询
&lowRange={lowRange?}
&highRange={highRange?}
&searchType={searchType}    #Specifies the search type: image 
&fileType={fileType?} # operator in Google Search to limit results to a specific file type can returns images of a specified type. Some of the allowed values are: bmp, gif, png, jpg, svg, pdf, ... 
&rights={rights?}
&imgSize={imgSize?} #Returns images of a specified size :huge,icon,large,medium,small,xlarge,xxlarge
&imgType={imgType?} #Returns images of a type :clipart,face,lineart,news,photo
&imgColorType={imgColorType?}   #Returns black and white, grayscale, or color images: mono, gray, and color. 
&imgDominantColor={imgDominantColor?}   #Returns images of a specific dominant color :black,blue,brown,gray,green,pink,purple,teal,white,yellow
&key={YOUR_API_KEY}
&alt=json]
'''

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

def down_img(url, img_type, key_word, x):
    headers = {}
    headers['User-Agent'] = user_agent()

    cur_path = os.path.abspath(os.curdir)
    goal_path = cur_path + '/image_' +key_word
    if  not os.path.exists(goal_path):
        os.mkdir('image_'+ key_word)
    try:
        res = requests.get(url, headers=headers, timeout=5)
    except Exception as e:
        print(e)
        #print(x)
        #continue
    else:
        res.encoding = 'utf-8'
        html = res.content
        if IsValidImage4Bytes(html):
            print("正在下载第%s张"%(x+1))
            loc = goal_path +'/'+str(x) + '.' +img_type
            with open(loc, "w") as f:
                f.write(html)
            #j += 1
        else:
            print("false")
            #continue


def IsValidImage4Bytes(buf):
  bValid = True
  try:
    Image.open(io.BytesIO(buf)).verify()
  except:
    bValid = False
  return bValid


def main():
    key_word = raw_input("爬取关键字")
    #num = raw_input("爬取数量(30倍数)")
    cx = "001883515226962144273%3Awspeqvtkpfs"
    key = "AIzaSyAAqydVROyHH2Xq_y2u2NOlCa9rFUlQ8Qg"
    #imgSize = ""
    #imgType = ""
    #imgColorType = ""
    #imgDominantColor = ""
    #fileType = ""
    i = 1
    img_url = []
    #print(num)
    url = "https://www.googleapis.com/customsearch/v1?q="+ key_word +"&num=10&start="+ str(i) +"&cx="+ cx +"&key="+ key +"&searchType=image&alt=json"#+"&imgSize="+ imgSize +"&imgType="+ imgType +"&imgColorType="+ imgColorType +"&imgDominantColor="+ imgDominantColor +"&fileType="+ fileType 
    html = str(load_page(url))
    #json = []
    js = json.loads(html)
    #print(js["items"][0]["link"])#图片url
    #print(js["items"][0]["mime"][js["items"][0]["mime"].rfind('/')+1:])#图片格式
    for x in xrange(0,10):
        img_url = js["items"][x]["link"]
        img_type = js["items"][x]["mime"][js["items"][x]["mime"].rfind('/')+1:]
        down_img(img_url, img_type, key_word, x)  

    

    #print(js['items'])
    #js_items = json.loads(tem)
    #print(js_items)
    

    #获取图片链接
    '''while (int(i) <= (int(num) - 30)):
        url = "https://www.googleapis.com/customsearch/v1?q="+ key_word +"&num=10&start="+ str(i) +"&cx="+ cx +"&imgSize="+ imgSize +"&imgType="+ imgType +"&imgColorType="+ imgColorType +"&imgDominantColor="+ imgDominantColor +"&key="+ key +"&fileType="+ fileType +
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
            if IsValidImage4Bytes(html):
                print("正在下载第%s张"%j)
                with open(loc, "w") as f:
                    f.write(html)
                j += 1
            else:
                print("false")
                continue
                

 	    

        #print(file_type)
        #img = load_page(x)
'''



if __name__ == '__main__':
    main()