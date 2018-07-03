# -*- coding: UTF-8 -*-
from PIL import Image
import cv2
import cv2.cv as cv
import numpy as np
#phash算法
#缩小图片：32 * 32是一个较好的大小，这样方便DCT计算
#转化为灰度图：把缩放后的图片转化为256阶的灰度图。（具体算法见平均哈希算法步骤）
#计算离散余弦变换(DCT):DCT把图片分离成分率的集合
##缩小DCT：DCT计算后的矩阵是32 * 32，保留左上角的8 * 8，这些代表的图片的最低频率
#计算平均值：计算缩小DCT后的所有像素点的平均值。
#进一步减小DCT：大于平均值记录为1，反之记录为0.
#得到信息指纹：组合64个信息位，顺序随意保持一致性。
#最后比对两张图片的指纹，获得汉明距离即可。

def get_phash(img_dir):
    #重新改变大小为32×32的灰度图
    img = cv2.imread(img_dir, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img,(32,32))
    #cv2.imshow('image', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    dct = cv2.dct(np.float32(img))
    
    dct.resize(8,8)
    print(dct)
    avg_dct = np.mean(dct)
    print(avg_dct)
    hash_num = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] >avg_dct:
                hash_num.append(1)
            else:
                hash_num.append(0)
    #print(hash_num)
    return hash_num            
def Hamming_distance(hash1, hash2):
    num = 0
    for x in range(len(hash1)):
         if hash1[x] == hash2[x]:
              num += 1
    return num
    

def main():
    hash1 = get_phash("./image_piano+movie/1_4.jpeg")
    hash2 = get_phash("./image_piano+movie/9_0.jpeg")
    print(Hamming_distance(hash1, hash2))
if __name__ == '__main__':
    main()