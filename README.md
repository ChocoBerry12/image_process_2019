# 에어마우스
* made by 김민수
* 2019 년 1 학기 기계정보공학특강1 디지털 이미지 처리 과목 프로젝트
>영상처리 알고리즘과 다각형 알고리즘으로 마우스 없이 마우스 조종하는 어플리케이션.

##  !!warning!!

* 이 프로젝트는 `python 3` 와 `pyautogui`, `opencv` 패키지가 사용되었음을 밝힙니다.
* 또한 제작자의 PC 는 window 10 환경에서 테스트 되었습니다. 

* 프로젝트를 실행하려면 위 3 개의 컴포넌트를 설치해야합니다.

pip 나 anoconda 터미널에서

    pip install opencv-python
    pip install pyautogui

명령어로 설치합니다.

## 사전지식
* convex hull [참고](https://ko.wikipedia.org/wiki/%EB%B3%BC%EB%A1%9D_%EA%BB%8D%EC%A7%88_%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98)
> **볼록 껍질 알고리즘**은 다양한 객체에  [볼록 껍질](https://ko.wikipedia.org/wiki/%EB%B3%BC%EB%A1%9D_%ED%8F%90%ED%8F%AC "볼록 폐포")을 만드는 알고리즘이다. 볼록 껍질 알고리즘은 수학 및 컴퓨터 과학에 광범위하게 적용되고 있다.

![convex hullì— ëŒ€í•œ ì´ë¯¸ì§€ ê²€ìƒ‰ê²°ê³¼](https://miro.medium.com/max/1354/1*F4IUmOJbbLMJiTgHxpoc7Q.png)

## 프로그램 플로우
1. background substraction
2. video 획득
3. convex 획득
4. convex 결함 검출
5. 손 중심 계산
6. 커맨드 결함 갯수로 커맨드 인식
7. 마우스 컨트롤
8. 반복

## 사용법
1. 코드를 실행시킨다
2. 웹캠으로 촬영되는 영상을 화면으로 확인한다.
3. 화면 우측은 손가락을 인식시킬 공간이므로 비워둔다.
4. 우측 공간이 비워졌으면 키보드 `q` 를 눌러 진행한다.
5. 화면 우측에는 손 말고 다른 움직이는 물체가 잡히면 안된다. 이를 유의하며 에어마우스를 사용한다.

## 커맨드 가이드
* translate - 검지와 엄지 편 상태
	* 손 중심 이동 = 마우스 포인터 translate
* left pointer - translate 상태에서 엄지를 접음
	* 1 회 접었다 펴기
		* left click
	* 엄지를 접은 채 이동
		* drag
* right pointer - 검지, 엄지, 중지 편 상태
	* right click
