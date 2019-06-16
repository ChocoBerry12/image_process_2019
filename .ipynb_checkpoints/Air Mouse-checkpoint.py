#!/usr/bin/env python
# coding: utf-8

# # 2019 DIP 프로젝트 - 2013430009 김민수
# ---
# 
# ## 에어 마우스
# >opencv 라이브러리와 마우스포인터 api 를 사용해 간단한 에어마우스 제작. 오브젝트(손)을 인식하고 좌표를 얻어 그 좌표로 포인터를 제어한다.
# 
# * convex hull
# * convexity defects
# * erosion
# * gaussian blurring
# * absolute substraction
# * contours
# ---

# ## opencv 와 마우스 api 불러오기

# In[4]:


import pyautogui
import cv2
import numpy as np


# ## 마우스 컨트롤 함수

# In[5]:


def control_mouse(num_defects, point, is_down_left):
    
    # 결함이 3 개 일때 좌 포인터 Down
    if(num_defects == 3):
        #pyautogui.click(button='left')
        if(not is_down_left):
            pyautogui.mouseDown(button='left')
            is_down_left = True
        else:
            pyautogui.moveTo(point)
        
    # 5 개 일때 우클릭
    elif(num_defects == 5):
        pyautogui.mouseUp(button='right')
        
    # 4 개 일때 포인터 이동
    elif(num_defects == 4):
        if(is_down_left):
            pyautogui.mouseUp(button='left')
            is_down_left = False
            
        # 포인터 이동
        pyautogui.moveTo(point)
        
    return is_down_left


# ## 루틴

# In[9]:


# 마우스 포인터 화면밖으로 나가게 허용
pyautogui.FAILSAFE = False

# 영상 
cap = cv2.VideoCapture(0)
cap.set(3,600)
cap.set(4,800)

back = None
flag_l = False

# 삭제할 배경 설정
while(True):
    ret, frame = cap.read()
    
    # 좌우 뒤집기
    frame = cv2.flip(frame, 1)
    cv2.imshow('background', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        back = frame[100:-1, 250:800]
        break
        
        
while(True):
    ret, frame = cap.read()

    if (ret):
        frame = cv2.flip(frame, 1)
        frame = frame[100:-1, 250:800]
        
        # 앞서 저장한 배경이미지를 매 프레임마다 빼줌.
        frame = cv2.absdiff(frame, back)
        
        cv2.imshow('diff', frame)
        
        # 배경이 극단적인 만약의 경우를 대비해 dilate 연산을 통해 뭉개기
        kernel = np.ones((5, 5), np.uint8)
        dilate = cv2.dilate(frame, kernel, iterations = 1)
        
        # 손이 분리되면 그 상태로 gray scale 변환
        gray = cv2.cvtColor(dilate, cv2.COLOR_BGR2GRAY)

        # binary 로 변환
        ret, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_OTSU)
        cv2.imshow('bin', binary)

        # 노이즈 제거
        blur = cv2.GaussianBlur(binary, (35, 35), 0)
        cv2.imshow('blur', blur)

        # 뭉툭한 이미지를 erode 연산으로 가늘게 하기
        erosion = cv2.erode(blur, kernel, iterations = 1)
        cv2.imshow('erode', erosion)

        #threshold를 이용하여 선명하게 다시 binary image로 변환
        ret, thresh = cv2.threshold(erosion, 127, 255, 0)
        
        # binary 영상에서 오브젝트의 테두리를 찾는다.
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        #외곽선을 표시한다.
        image = cv2.drawContours(frame, contours, -1, (0,255,0), 3)
        
        # 테두리가 있을 때
        if(len(contours) > 0):
            
            # 첫번째 외곽선 저장
            cnt = contours[0] 
            
            # 볼록껍질 알고리즘으로 손바닥 인식
            hull = cv2.convexHull(cnt, returnPoints=False)
            
            # convex 결함을 찾아 저장
            defects = cv2.convexityDefects(cnt,hull)
            
            # 결함이 있으면
            if(defects is not None):
                x_center = 0
                y_center = 0
                num = 0
                
                for i in range(defects.shape[0]):
                    # s 는 시작점, e 는 끝점, f 는 결점, d 는 결점의 깊이
                    s,e,f,d = defects[i,0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    cv2.line(frame, start, end, [0, 0, 255], 3)
                    
                    # 결점의 깊이가 일정수준 이상이면 손가락 사이라고 판단
                    if(d > 1000):
                        num += 1
                        cv2.circle(frame, far, 5, [255, 0, 255], -1)
                        #cv2.circle(frame,end,5,[255,0,0],-1)
                        cv2.circle(frame,start,5,[40*i,40*i,40*i],-1)

                        x_center += far[0]
                        y_center += far[1]
                        #print(far[0], far[1])
                        
                # 손가락 사이를 하나도 검출 못하면 넘어감
                if(num == 0):
                    pass
                
                # 
                else:
                    x_center /= num
                    y_center /= num
                    cv2.circle(frame, (int(x_center), int(y_center)) ,5,[0, 255, 255], -1)
                    #cv2.circle(frame, point ,10, [0,255,255],-1)
                    point = ((x_center - 130) * 8.5, (y_center - 140) * 5)
                    
                    # 마우스 컨트롤
                    flag_l = control_mouse(num, point, flag_l)
                    
                    info = "center pos : {}, {} | mouse pos : {}, {}".format(int(x_center), int(y_center), point[0], point[1])
                    cv2.putText(image, info, (5, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                    num_def = "defects counts : {}".format(num)
                    cv2.putText(image, num_def, (5, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                    flag = "left button Down : {}".format(flag_l)
                    cv2.putText(image, flag, (5, 60), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                    
        else:
            print('손 없음')
        

        cv2.imshow('image', image)
        cv2.imshow('ime', thresh)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

