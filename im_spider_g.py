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
import argparse
import dhash
import time
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
    res = requests.get(url, headers=headers,timeout=30)
    res.encoding = 'utf-8'
    html = res.text
    return html

#判断图片是否完整
def IsValidImage4Bytes(buf):
  bValid = True
  try:
    Image.open(io.BytesIO(buf)).verify()
  except:
    bValid = False
  return bValid

#获取图片类型
def get_img_type(buf):
    img_type = Image.open(io.BytesIO(buf)).format
    return img_type 


def main():
    #添加命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument("-isize", "--imgSize", help="图片大小 可选 huge, icon, large, medium, small, xlarge, xxlarge")
    parser.add_argument("-itype", "--imgType", help="图片类型 可选 clipart, face, lineart, news, photo")
    parser.add_argument("-icolor", "--imgColorType", help="图片色彩类型 可选 mono, gray, color")
    parser.add_argument("-idcolor", "--imgDominantColor", help="图片主色调 可选 black, blue, brown, gray, green, pink, purple, teal, white, yellow, red, orange")
    parser.add_argument("-ft", "--fileType", help="图片格式 可选 bmp, gif, png, jpg")
    args = parser.parse_args()
    url = "https://www.googleapis.com/customsearch/v1?"
    if args.imgSize:
        url = url + "&imgSize="+ args.imgSize
    if args.imgType:
        url = url + "&imgType="+ args.imgType
    if args.imgColorType:
        url = url + "&imgColorType="+ args.imgColorType
    if args.imgDominantColor:
        url = url + "&imgDominantColor="+ args.imgDominantColor
    if args.fileType:
        url = url + "&fileType="+ args.fileType 


    key_word = raw_input("爬取关键字")
    cx = "001883515226962144273%3Awspeqvtkpfs"
    key = "AIzaSyAAqydVROyHH2Xq_y2u2NOlCa9rFUlQ8Qg"
    num = int(raw_input("爬取数量"))/10
    url = url + "&q=" +key_word +"&num=10&filter=1&cx="+ cx +"&key="+ key +"&searchType=image&alt=json&start="
    i = 1
    start = i
    #创建下载目录
    cur_path = os.path.abspath(os.curdir)
    goal_path = cur_path + '/image_' +key_word
    if  not os.path.exists(goal_path):
        os.mkdir('image_'+ key_word)
    dic = ["jpg","png","JPEG","jpeg","JPG","PNG","bmp","BMP"]
    while i <= num:

        full_url = url + str(start)
        html = str(load_page(full_url))
        js = json.loads(html)
           
        #获取图片链接及图片类型
        for x in xrange(0,10):
            try:
                img_url = js["items"][x]["link"]
                #print("获取图片url：" + img_url)
            except Exception as e:
                print("获取图片url失败")
                continue
            
            #img_type = js["items"][x]["mime"][js["items"][x]["mime"].rfind('/')+1:]
        
            
            #下载图片
            headers = {}
            headers['User-Agent'] = user_agent()
            try:
                res = requests.get(img_url, headers=headers, timeout=30)
            except Exception as e:
                print(e)
                print("连接错误")
                continue
            else:
                res.encoding = 'utf-8'
                con = res.content
                if IsValidImage4Bytes(con):
                    
                    img_type = get_img_type(con).lower()
                    if not img_type in dic:
                        continue

                    loc = goal_path +'/'+ str(i) + "_" + str(x) + '.' +img_type
                    print("正在下载第%s组%s张"%(i, x+1))
                    with open(loc, "w") as f:
                        f.write(con)
                    print("下载完成")
                    
                else:
                    print("图片错误")
                    continue
        
        i += 1
        start += 10
    print("开始去重")
    start = time.time()   
    dhash.remove_file(goal_path)
    end = time.time()
    print("用时:"+str((end-start)/60))


if __name__ == '__main__':
    main()