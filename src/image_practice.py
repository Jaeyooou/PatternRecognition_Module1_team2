import cv2
import numpy as np

# canny dectection
#1 단계: 노이즈제거(가우시안 필터로)
#2 단계 :Gradient 값이 높은 부분 찾기
# 3단계 : 최대값이 아닌 픽셀의 값을 0 으로 만들기
# 4단계 : Hyteresis Thresholding : 3단계를 거친 이미지가 실제 엣지인지 판단하는 부분

path= 'resource/0.png'
image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
Canny_image = cv2.Canny(image , 50 , 200)


cv2.imshow('original' , image)
cv2.imshow('canny_img',Canny_image)

cv2.waitKey(0)
cv2.destroyWindow()