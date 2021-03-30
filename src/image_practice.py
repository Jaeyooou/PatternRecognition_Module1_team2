import cv2
import numpy as np

# canny dectection
#1 단계: 노이즈제거(가우시안 필터로)
#2 단계 :Gradient 값이 높은 부분 찾기
# 3단계 : 최대값이 아닌 픽셀의 값을 0 으로 만들기
# 4단계 : Hyteresis Thresholding : 3단계를 거친 이미지가 실제 엣지인지 판단하는 부분
def FindContour(path):
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
          crop_img = src[y:y+h , x:x+w] # 직사각형 기준으로 자른 이미지
          crop_upper_img = cv2.resize(crop_img , (400,400)) # 자른이미지 400*400 으로 확대
          print(x , y,  w, h) # 컨투어 좌표 x , y, 가로 , 세로
          break # 만약 숫자 안에 도형이 하나 더 있으면 안찍히게 하기 위해서

######################################### 출력부분
     cv2.imshow("src",src) # 원본
     cv2.imshow("contour_image" , contour_src) # 컨투어한 사각형 이미
     cv2.imshow("crop",crop_img)
     cv2.imshow("crop & upper" , crop_upper_img)

     cv2.waitKey(0)
     cv2.destroyWindow()


path= 'resource/Godic/8.png'
FindContour(path)
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
