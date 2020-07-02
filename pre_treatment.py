import cv2,os
import matplotlib.pyplot as plt
import hashlib
import numpy as np

from skimage.filters import threshold_yen
from skimage.exposure import rescale_intensity
from skimage.io import imread, imsave
img_path=r'/home/cver/lcx/Part_Classification/HPT/burn-BR20160016-1.png'
gpath=r'/home/cver/lcx/Part_Classification/HPT/burn-BR20160016-0.png'
# path=r'/home/cver/lcx/Part_Classification/HPT'
path=r'/home/cver/lcx/temp/trainimg'
path_list = [os.path.join(path,name) for name in os.listdir(path)[:19]]
def showimg(img1,img2):#按一行两列的格式输出图像，适合jupyter界面
#     plt.figure(figsize=(img.shape[0]/50, img.shape[1]/50))
    plt.figure(figsize=(img.shape[0]/10, img.shape[1]/10))
    plt.subplot(1,2,1)
    plt.axis('off');plt.imshow(img1)
    plt.subplot(1,2,2)
    plt.axis('off');plt.imshow(img2)
    plt.show()
def loadimg(img_path):
    return imread(img_path)
def yen(img):#适合处理扫描件，提升图像亮度和细节https://scikit-image.org/docs/dev/api/skimage.filters.html#threshold-yen
    yen_threshold = threshold_yen(img)
    bright = rescale_intensity(img, (0, yen_threshold), (0, 255))
    return bright
def clahe(img):#限制对比度自适应直方图均衡(Contrast Limited Adaptive Histogram Equalization），适合去雾、提升饱和度对比度
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    lab_planes = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(1,1))
    lab_planes[0] = clahe.apply(lab_planes[0])
    lab = cv2.merge(lab_planes)
    dst = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return dst
def canny(img):
    dst=cv2.Canny(img,70,250)
    return dst
def guidedFilter(img): #向导滤波
    dst = cv2.ximgproc.guidedFilter(img,img,60,1000)
    return dst
def bm3d(img):#####有专利限制
    dst = cv2.xphoto.bm3dDenoising(img)
    return dst
def mean(img):#减均值后，图像的背景部分会变白，这是叫‘白化（whiten）’吗
#     print(type(img),img.dtype)
    sub_img = np.zeros(shape=img.shape, dtype=np.uint8)
    mean = [95,93,87]
#     mean = [103,116,128]
    sub_img[:,:,0] += mean[0]
    sub_img[:,:,1] += mean[1]
    sub_img[:,:,2] += mean[2]
    return sub_img
#     print(sub_img[:,:,0])
    
#     dst = img[:,:,0] - (95,93,87)
    
for i in path_list:
    img = loadimg(i)
    dst = mean(img)
    dst1 = clahe(img)
    dst2 = dst1 - dst
#     print(dst)
#     dst = cv2.fastNlMeansDenoisingColored(img)
#     dst1 = canny(img)
#     dst2 = canny(dst)
    showimg(dst1,dst2)
