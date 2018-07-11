# -*- coding: UTF-8 -*-
from PIL import Image
import os, sys
#1.缩小图片：收缩到9*8的大小，一遍它有72的像素点

#2.转化为灰度图：把缩放后的图片转化为256阶的灰度图。（具体算法见平均哈希算法步骤）

#3.计算差异值：dHash算法工作在相邻像素之间，这样每行9个像素之间产生了8个不同的差异，一共8行，则产生了64个差异值

#4.获得指纹：如果左边的像素比右边的更亮，则记录为1，否则为0.


def get_dhash(loc):
    rwidth = 9
    rheight = 8
    img = Image.open(loc)
    img = img.resize((rwidth, rheight), Image.ANTIALIAS).convert('L')
    pix = list(img.getdata())
    dif = []
    for i in range(rheight):
        start = i * rwidth
        for j in range(rwidth - 1):
            left_pix = start + j
            if pix[left_pix] > pix[left_pix + 1]:
                dif.append(1)
            else:
                dif.append(0)
    return dif
    '''for x in range(8):
        #print(type(dif[x:x+8]))
        str_dif = "".join(map(str, dif[x:x+8]))
        print(hex(int(str_dif, 2)))'''
    #if dif % 8 == 7:  # 每8位的结束        
   # hash_string += str(hex(decimal_value)[2:].rjust(2, "0"))
def Hamming_distance(hash1, hash2):
    num = 0
    for x in range(len(hash1)):
         if hash1[x] != hash2[x]:
              num += 1
    return num

def remove_file(path):
    #hash1 = get_dhash("./image_piano+movie/1_6.jpeg")
    #hash2 = get_dhash("./image_piano+movie/1_7.jpeg")
    #print(Hamming_distance(hash1, hash2))
    #path = os.path.abspath(os.curdir)+"/"+file_name
    dirs = os.listdir( path )
    for file1 in dirs:
        for file2 in dirs:
            if file2 != file1:
                try:
                    hash1 = get_dhash(path + "/" + file1)
                    hash2 = get_dhash(path + "/" +  file2)
                except Exception as e:
                    continue

                if Hamming_distance(hash1, hash2)<20:
                    try:
                        os.remove(path + "/" + file2)
                        dirs.remove(path + "/" + file2)
                    except Exception as e:
                        continue
                    
if __name__ == '__main__':
    main()