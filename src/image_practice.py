import cv2
import numpy as np
from matplotlib import pyplot as plt
# canny dectection
#1 단계: 노이즈제거(가우시안 필터로)
#2 단계 :Gradient 값이 높은 부분 찾기
# 3단계 : 최대값이 아닌 픽셀의 값을 0 으로 만들기
# 4단계 : Hyteresis Thresholding : 3단계를 거친 이미지가 실제 엣지인지 판단하는 부분
def Resize(path):
     src = cv2.imread(path , cv2.IMREAD_COLOR)
     contour_src = src.copy()
     gray = cv2.cvtColor(src , cv2.COLOR_BGR2GRAY)
     ret,binary = cv2.threshold(gray , 127 , 255 , cv2.THRESH_BINARY)
     binary = cv2.bitwise_not(binary)
     contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     print(len(contours))
     for cnt in contours:
          x , y, w , h = cv2.boundingRect(cnt)
          cv2.rectangle(contour_src ,(x,y) , (x+w,y+h) ,(0,255,0) ,1) # 초록색으로 컨투어 검출해서 직사각형 찍기
          crop_img = src[y:y+h , x:x+w].copy() # 직사각형 기준으로 자른 이미지
          crop_upper_img = cv2.resize(crop_img ,None , fx =2.0 , fy = 2.0 ,  interpolation=cv2.INTER_CUBIC) # 자른이미지 fx , fy 비율로 확대
          height , width = crop_upper_img.shape[:2]
          print("height , width :" +str(height) + str(width))
          print(x , y,  w, h) # 컨투어 좌표 x , y, 가로 , 세로
          break # 만약 숫자 안에 도형이 하나 더 있으면 안찍히게 하기 위해서

######################################### 출력부분
     # cv2.imshow("src",src) # 원본
     # cv2.imshow("w",white_img)
     # cv2.imshow("contour_image" , contour_src) # 컨투어한 사각형 이미
     # cv2.imshow("crop",crop_img)
     # cv2.imshow("crop & upper" , crop_upper_img)
     # cv2.waitKey(0)
     return crop_upper_img

def GousianFilter(img):
     blur = cv2.GaussianBlur(img , (11,11) , 0)
     return blur;

def prac(img):
     height , width = img.shape[0:2]
     for w in range(0 , width):
          print(img[0,w]);

def findDiagonalDirection(img,flag):

    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    images = np.zeros((28,28))
    flatten = imgray.flatten() / 255.0

    i = 0
    j = 0
    for i in range(28):
        for j in range(28):
            images [i,j] ="%0.1f"%flatten[28*i+j]

    #2/35를 구별하기 위한 임계값


    #임의로 16
    if flag == 1:
        median = 16
    else :
        median = 8

    for i in range(28):
        if(images[median,i]!=0):
            #print(images[19,i], i,end=" ")
            if(i<14):
                if flag == 1:
                    return 2
                else :
                    return 5
            if(i>14):
                return 3
    return 0

def FindContours(img):
     img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
     ret , imthres = cv2.threshold(img_gray , 127, 255 , cv2.THRESH_BINARY_INV)
     contour, hierarchy = cv2.findContours(imthres, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
     # 가장 바깥쪽 컨투어에 대해 꼭지점 좌표만 반환 ---④
     contour2, hierarchy = cv2.findContours(imthres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
     # 각각의 컨투의 갯수 출력 ---⑤
     print('도형의 갯수: %d(%d)' % (len(contour), len(contour2)))
def FindWhitePx(img):
     #2 와 3 을 구분하는 함수
     height, width = img.shape[0:2]
     img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
     # 임계값 처리한 이미지 , 127 보다 높으면 255 , 아니면 0
     ret, imthres = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV) # binary image 로 변형
     cnt = 0 # white px 개수
     white_area = 0; # 면적의 퍼센트
     for w in range(0,width):
          if imthres[height-1,w] == 255:
               cnt = cnt+1
     white_area = cnt / width * 100
     if white_area < 40 :
          print("this image is 3")
     else :
          print("this image is 2")


# 고딕3 : 28   27.692307692307693 %
# 굴림3 : 39   31.451612903225808 %
# HY3 : 28    36.84210526315789 %


# 고딕2 :128    100.0 %
# 굴림2 :119    99.16666666666667 %
# HY2:70       89.74358974358975 %


if __name__ == '__main__':
     path= 'resource/HY/2.png' #이미지 입력
     resize_img = Resize(path)
     Gousian_img = GousianFilter(resize_img)
     FindWhitePx(Gousian_img)

     cv2.waitKey(0)

















# dst = src.copy()
# gray = cv2.cvtColor(src , cv2.COLOR_BGR2GRAY)
# canny = cv2.Canny(gray , 5000 , 1500 , apertureSize=5 , L2gradient= True)
# lines = cv2.HoughLinesP(canny, 0.8, np.pi / 180, 90, minLineLength = 10, maxLineGap = 100)
#
# for i in lines:
#     cv2.line(dst, (i[0][0], i[0][1]), (i[0][2], i[0][3]), (0, 0, 255), 2)
#
# cv2.imshow('original' , src)
# cv2.imshow('gray_img',gray)
# cv2.imshow('canny_img' , canny)
