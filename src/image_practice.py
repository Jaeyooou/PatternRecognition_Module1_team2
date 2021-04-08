import cv2
import numpy as np
from matplotlib import pyplot as plt
# canny dectection
#1 단계: 노이즈제거(가우시안 필터로)
#2 단계 :Gradient 값이 높은 부분 찾기
# 3단계 : 최대값이 아닌 픽셀의 값을 0 으로 만들기
# 4단계 : Hyteresis Thresholding : 3단계를 거친 이미지가 실제 엣지인지 판단하는 부분
#################################################################################


# 내부도형 검출하는 코드 컨투어가 1이면 내부도형 x , 2 이상이면 내부도형 존재
def FindContours(img):  # 컨투어의 개수
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, imthres = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
    contour, hierarchy = cv2.findContours(imthres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # 가장 바깥쪽 컨투어에 대해 꼭지점 좌표만 반환 ---④
    contour2, hierarchy = cv2.findContours(imthres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 각각의 컨투의 갯수 출력 ---⑤
    print('도형의 갯수: %d(%d)' % (len(contour), len(contour2)))
    if (len(contour2) == 1):
        return False
    else:
        return True


#컨투어가 2 이상일 때 -> 내부도형 존재할 때 , 8/0,4,6,9 판단
def Find_Center_of_Gravity(src):
    contour_src = src.copy()
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    ret, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    binary = cv2.bitwise_not(binary)
    contours = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

    if (len(contours) == 3): # 검출 3개 , 숫자 1개 ,내부도형 2개
        return 8
    elif (len(contours) == 2):# 검출 2개  , 숫자 1개 , 내부도형 1개
        M = cv2.moments(contours[0])  # 숫자의 무게중심
        cX_1 = int(M['m10'] / M['m00'])
        cY_1 = int(M['m01'] / M['m00'])

        M = cv2.moments(contours[1])  # 숫자 내부 도형의 무게중심
        cX_2 = int(M['m10'] / M['m00'])
        cY_2 = int(M['m01'] / M['m00'])
        print(cX_1, cX_2, cY_1, cY_2)

        if cX_1 == cX_2 and cY_1 == cY_2:
            return 0;
        # 두 무게중심을 지나는 직선의 기울기 1미만이면 숫자 4
        elif (cX_1 - cX_2) != 0 and (cY_1 - cY_2) / (cX_1 - cX_2) < 1:
            cv2.line(src, (cX_1, cY_1), (cX_2, cY_2), (0, 255, 0), 1)
            return 4
        elif cY_1 < cY_2:
            return 6
        else:
            return 9


def Find_Center_of_Gravity2(src):
    contour_src = src.copy()
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    binary = cv2.bitwise_not(binary)
    contours = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
    height, width = src.shape[:2]
    M = cv2.moments(contours[0])
    cY_weight = int(M['m01'] / M['m00'])
    cY_rate = cY_weight / height
    print("이미지 height :" + str(height) )
    print("무게중심 y 좌표 :" + str(cY_weight))
    print("무게중심 y 좌표 / height (비율 ) : " + str(cY_rate))

    # height/width/ height/width :
    # 5#hy# 0.4918032786885246#goolim#0.4956521739130435#godic#0.49107142857142855
    # 7#hy#0.36065573770491804#goolim# 0.3577586206896552#godic#0.37383177570093457

    if (cY_rate >0.45):
        return 5
    else:
        return 7
def Find_heigth_width_rate(img):
    height, width = img.shape[:2]
    rate = height / width
    if rate >= 2:
        return True
    else :
        return False

#    # height/width/ height/width :
    # 1#hy#116/58/2.0#goolim#236/50/4.72#godic#220/82/2.682926829268293
    # 2#hy#122/78/1.564102564102564#goolim#228/120/1.9#godic#226/128/1.765625
    # 3#hy#124/76/1.631578947368421#goolim#234/124/1.8870967741935485#godic#230/130/1.7692307692307692


# 아랫부분 숫자가 맞닿는 픽셀 면적으로  2 와 3 을 구분하는 함수
def Find_bottom_WhitePx(img):
    height, width = img.shape[0:2]
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 임계값 처리한 이미지 , 127 보다 높으면 255 , 아니면 0
    ret, imthres = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)  # binary image 로 변형
    cnt = 0  # white px 개수
    white_area = 0;  # 면적의 퍼센트
    for w in range(0, width):
        if imthres[height - 1, w] == 255:
            cnt = cnt + 1
    white_area = cnt / width * 100
    if white_area < 60:
        print("3")
    else:
        print("2")
    # 고딕3 : 28   27.692307692307693 %
    # 굴림3 : 39   31.451612903225808 %
    # HY3 : 28    36.84210526315789 %

    # 고딕2 :128    100.0 %
    # 굴림2 :119    99.16666666666667 %
    # HY2:70       89.74358974358975 %

def Find_top_Whitepx(img):
    height, width = img.shape[0:2]
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 임계값 처리한 이미지 , 127 보다 높으면 255 , 아니면 0
    ret, imthres = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)  # binary image 로 변형
    cnt = 0  # white px 개수
    white_area = 0;  # 면적의 퍼센트
    for w in range(0, width):
        if imthres[0, w] == 255:
            cnt = cnt + 1
    white_area = cnt / width * 100
    print(white_area)
    if white_area > 70 :
        # 5,7 둘중 하나 임
        return True
    else:
        #1,2,3 셋중 하나
        return False

#    ##########
#
# 판단부분
#
#  #############################

def GousianFilter(img):
     blur = cv2.GaussianBlur(img , (11,11) , 0) # 11,11 부분 크면 클수록 부드러워짐
     return blur;


def Resize(src):
    contour_src = src.copy()
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    binary = cv2.bitwise_not(binary)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print(len(contours))
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(contour_src, (x, y), (x + w, y + h), (0, 255, 0), 1)  # 초록색으로 컨투어 검출해서 직사각형 찍기
        crop_img = src[y:y + h, x:x + w].copy()  # 직사각형 기준으로 자른 이미지
        crop_upper_img = cv2.resize(crop_img, None, fx=2.0, fy=2.0,
                                    interpolation=cv2.INTER_CUBIC)  # 자른이미지 fx , fy 비율로 확대
        height, width = crop_upper_img.shape[:2]
        print("height , width :" + str(height) +"/" +  str(width))
        print(x, y, w, h)  # 컨투어 좌표 x , y, 가로 , 세로
        print(height / width)
        break  # 만약 숫자 안에 도형이 하나 더 있으면 안찍히게 하기 위해서

    ######################################### 출력부분
    # cv2.imshow("src",src) # 원본
    # cv2.imshow("w",white_img)
    # cv2.imshow("contour_image" , contour_src) # 컨투어한 사각형 이미
    # cv2.imshow("crop",crop_img)
    # cv2.imshow("crop & upper" , crop_upper_img)
    # cv2.waitKey(0)
    return crop_upper_img


if __name__ == '__main__':
     path= 'resource/godic/1.png' #이미지 입력
     src = cv2.imread(path)


     #Gousian_img = GousianFilter(resize_img)
     #Find_top_Whitepx(Gousian_img)

     if FindContours(src) == True: # 0,4,6,8,9 판단
        print(Find_Center_of_Gravity(src))
     elif FindContours(src) == False:#1,2,3,5,7 판단
         resize_img = Resize(src)
         Gousian_img = GousianFilter(resize_img)
         if Find_top_Whitepx(Gousian_img) == True:# 5,7 판단
             #숫자의 윗면적이 70퍼센트를 차지한다고 한다면
            #무게중심 판단
            print(Find_Center_of_Gravity2(Gousian_img))
         elif Find_top_Whitepx(Gousian_img) == False:# 1,2,3 판단
             if Find_heigth_width_rate(Gousian_img) == True:
                 print(1)
             else:
                 Find_bottom_WhitePx(Gousian_img)
             #숫자의 윗면적이 70보다 낮으면
            # 가로세로 비율 판단




















