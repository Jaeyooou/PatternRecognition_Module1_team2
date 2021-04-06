import cv2
import numpy as np

#path = 'C:/Users/user/Desktop/v1/3fonts/gulim/4.png'
#path = 'C:/Users/user/Desktop/v1/3fonts/hyshin/4.png'
#path = 'C:/Users/user/Desktop/v1/3fonts/godic/7.png'
path = 'resource/goolim/4.png'
img = cv2.imread(path, cv2.IMREAD_COLOR)
img2 = img.copy()
# 그레이 스케일 변환 ---①
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 노이즈 제거를 위한 가우시안 블러 ---②
blur = cv2.GaussianBlur(gray, (3,3), 0)
# 허프 원 변환 적용( dp=1.2, minDist=30, cany_max=200 ) ---③
circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 4.7, 30, None, 200)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # 원 둘레에 초록색 원 그리기
        cv2.circle(img,(i[0], i[1]), i[2], (0, 255, 0), 2)
        # 원 중심점에 빨강색 원 그리기
        cv2.circle(img, (i[0], i[1]), 2, (0,0,255), 5)

# 결과 출력
merged = np.hstack((img, img2))
cv2.imshow('Probability hough line', merged)
cv2.waitKey()
cv2.destroyAllWindows()