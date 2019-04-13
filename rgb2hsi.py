#coding=utf-8
import cv2
import numpy as np

pi=3.141592653589793


def rgb2hsi(rgbImg):
    """
    这个是我自己写的。中间使用了一些python和numpy的矩阵操作，加快了运算速度。
    下面的代码是在网上找的，速度就比较慢。这里我一开始一直算出来的结果跟人家的不一样。
    花了好长时间才发现，我的公式是照着数字图像处理第三版写的，在计算theta时书中
    少写了一个括号，所以我算出来的结果一直不对。。。后来发现了改正了就好了。
    """
    hsiImg=rgbImg.copy() #h,w,c
    rgbImg=rgbImg/255.0
    b_img,g_img,r_img=rgbImg[:,:,0],rgbImg[:,:,1],rgbImg[:,:,2]
    h_img=s_img=i_img=np.zeros(r_img.shape)

    epsi=1e-6
    den_theta=np.sqrt((r_img-g_img)*(r_img-g_img)+(r_img-b_img)*(g_img-b_img))+epsi
    num_theta=((r_img-g_img)+(r_img-b_img))/2+epsi#《数字图像处理》书中共识少些了一个括号
    cos_theta=num_theta/den_theta 
    # try:
    #     theta=np.arccos(cos_theta)
    # except:
    #     print(cos_theta)
    theta=np.arccos(cos_theta)
    BG_valueCom=b_img<=g_img
    theta_part=theta*BG_valueCom
    complementary_part=(2*pi-theta)*(1-BG_valueCom)
    h_img=theta_part+complementary_part
    h_img=h_img/(2*pi)

    den_s=(r_img+b_img+g_img)+epsi
    num_s=3*np.minimum(np.minimum(r_img,b_img),g_img)+epsi
    s_img=1-num_s/den_s

    i_img=(r_img+b_img+g_img)/3

    hsiImg[:,:,0]=h_img*255.0
    hsiImg[:,:,1]=s_img*255.0
    hsiImg[:,:,2]=i_img*255.0

    return hsiImg


def hsi2rgb(hsiImg):
    """
    hsiImg需要已经归一化至01之间。
    """
    rgbImg=hsiImg.copy()
    h_img,s_img,i_img=hsiImg[:,:,0],hsiImg[:,:,1],hsiImg[:,:,2]
    h_img=h_img*2*pi
    first_section=h_img<(2*pi/3)
    second_section_=h_img<(4*pi/3)
    second_section=(1-first_section)*second_section_
    third_section=1-second_section_

    b_img_first=i_img*(1-s_img)
    r_img_first=i_img*(1+s_img*np.cos(h_img)/np.cos(pi/3-h_img))
    g_img_first=3*i_img-(r_img_first+b_img_first)

    h_img_second=h_img-2*pi/3
    r_img_second=i_img*(1-s_img)
    g_img_second=i_img*(1+s_img*np.cos(h_img_second)/np.cos(pi/3-h_img_second))
    b_img_second=3*i_img-(r_img_second+g_img_second)

    h_img_third=h_img-4*pi/3
    g_img_third=i_img*(1-s_img)
    b_img_third=i_img*(1+s_img*np.cos(h_img_third)/np.cos(pi/3-h_img_third))
    r_img_third=3*i_img-(b_img_third+g_img_third)

    b_img=b_img_first*first_section+b_img_second*second_section+b_img_third*third_section
    g_img=g_img_first*first_section+g_img_second*second_section+g_img_third*third_section
    r_img=r_img_first*first_section+r_img_second*second_section+r_img_third*third_section

    rgbImg[:,:,0]=b_img*255.0
    rgbImg[:,:,1]=g_img*255.0
    rgbImg[:,:,2]=r_img*255.0

    return rgbImg



def RGB2HSI2_fromInternet(rgb_img):
    """
    这是将RGB彩色图像转化为HSI图像的函数
    :param rgm_img: RGB彩色图像
    :return: HSI图像
    """
    #保存原始图像的行列数
    row = np.shape(rgb_img)[0]
    col = np.shape(rgb_img)[1]
    #对原始图像进行复制
    hsi_img = rgb_img.copy()
    #对图像进行通道拆分
    B,G,R = cv2.split(rgb_img)
    #把通道归一化到[0,1]
    [B,G,R] = [ i/ 255.0 for i in ([B,G,R])]
    H = np.zeros((row, col))    #定义H通道
    I = (R + G + B) / 3.0       #计算I通道
    S = np.zeros((row,col))      #定义S通道
    for i in range(row):
        den = np.sqrt((R[i]-G[i])**2+(R[i]-B[i])*(G[i]-B[i]))
        thetha = np.arccos(0.5*(R[i]-B[i]+R[i]-G[i])/den)   #计算夹角
        h = np.zeros(col)               #定义临时数组
        #den>0且G>=B的元素h赋值为thetha
        h[B[i]<=G[i]] = thetha[B[i]<=G[i]]
        #den>0且G<=B的元素h赋值为thetha
        h[G[i]<B[i]] = 2*np.pi-thetha[G[i]<B[i]]
        #den<0的元素h赋值为0
        h[den == 0] = 0
        H[i] = h/(2*np.pi)      #弧度化后赋值给H通道
    #计算S通道
    for i in range(row):
        min = []
        #找出每组RGB值的最小值
        for j in range(col):
            arr = [B[i][j],G[i][j],R[i][j]]
            min.append(np.min(arr))
        min = np.array(min)
        #计算S通道
        S[i] = 1 - min*3/(R[i]+B[i]+G[i])
        #I为0的值直接赋值0
        S[i][R[i]+B[i]+G[i] == 0] = 0
    #扩充到255以方便显示，一般H分量在[0,2pi]之间，S和I在[0,1]之间
    hsi_img[:,:,0] = H*255
    hsi_img[:,:,1] = S*255
    hsi_img[:,:,2] = I*255
    return hsi_img










