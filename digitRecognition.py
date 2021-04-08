import cv2
import numpy as np

#path = 'C:/Users/user/Desktop/v1/3fonts/gulim/9.png'
#path = 'C:/Users/user/Desktop/v1/3fonts/hyshin/9.png'
path = 'C:/Users/user/Desktop/v1/3fonts/godic/9.png'

src = cv2.imread(path, cv2.IMREAD_COLOR)
contour_src = src.copy()
gray = cv2.cvtColor(src , cv2.COLOR_BGR2GRAY)
ret,binary = cv2.threshold(gray , 127 , 255 , cv2.THRESH_BINARY)
binary = cv2.bitwise_not(binary)
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
num_contours = contours

for cnt in contours:
    x , y, w , h = cv2.boundingRect(cnt)
    cv2.rectangle(contour_src ,(x,y) , (x+w,y+h) ,(0,255,0) ,1)
    crop_img = src[y:y+h , x:x+w] # 직사각형 기준으로 자른 이미지
    crop_upper_img = cv2.resize(crop_img , (200,200)) # 자른이미지 200*200 으로 확대
    print(x , y,  w, h)
    break # 만약 숫자 안에 도형이 하나 더 있으면 안찍히게 하기 위해서


gray = cv2.cvtColor(crop_upper_img, cv2.COLOR_RGB2GRAY)
GSblur = cv2.GaussianBlur(gray, (11,11), 0)
ret, binary = cv2.threshold(GSblur, 150, 255, cv2.THRESH_BINARY_INV)
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

if len(num_contours) == 1 :
    # 허프 원 변환 적용
    circles = cv2.HoughCircles(GSblur, cv2.HOUGH_GRADIENT,1,20,param1=80,param2=26,minRadius=0,maxRadius=0)

    #원이 없을 경우
    if circles is None:
        #무게중심 판단
        M = cv2.moments(contours[0])
        cY_weight = int(M['m01'] / M['m00'])

        if (cY_weight < 80):
            print("7입니다")
        else:
            print("1입니다")

    #원이 있을 경우
    elif circles is not None:
        #꼭짓점 판단
        corners = cv2.goodFeaturesToTrack(GSblur, 10, 0.3, 15, blockSize=20, useHarrisDetector=True, k=0.03)
        for i in corners:
            cv2.circle(GSblur, tuple(i[0]), 3, (0, 0, 255), 2)
        if(len(corners)==6):
            print("5입니다")

        circles = np.uint16(np.around(circles))
        circleCount = 0
        for i in circles[0,:]:
            cv2.circle(GSblur,(i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(GSblur, (i[0], i[1]), 2, (0,0,255), 5)
            circleCount += 1
        print("원 개수 : ", circleCount)

elif len(num_contours) == 2 :
    #무게중심 0,4,6,9 구별
    M = cv2.moments(contours[0])
    cX_1 = int(M['m10'] / M['m00'])
    cY_1 = int(M['m01'] / M['m00'])
    cv2.circle(GSblur, (int(cX_1), int(cY_1)), 1, (255, 0, 0), -1)
    M = cv2.moments(contours[1]) #숫자 내부 도형의 무게중심
    cX_2 = int(M['m10'] / M['m00'])
    cY_2 = int(M['m01'] / M['m00'])
    cv2.circle(GSblur, (int(cX_2), int(cY_2)), 1, (255, 0, 0), -1)

    if abs(cY_1-cY_2)<2:
        print("0입니다")
    #두 무게중심을 지나는 직선의 기울기 1미만이면 숫자 4
    elif (cX_1-cX_2) != 0 and (cY_1-cY_2)/(cX_1-cX_2)<1:
        print("4입니다")
    elif cY_1 < cY_2:
        print("6입니다")
    else :
        print("9입니다")


# 무게중심 8 구별
elif len(num_contours) == 3 :
    print("8입니다")

cv2.imshow("dst", crop_upper_img)
cv2.waitKey(0)
cv2.destroyAllWindows()