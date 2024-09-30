
- 가상 피팅 시연 영상 https://drive.google.com/file/d/1stuLeTkFVn8PnnjIiRqj0D94JId0niGA/view?usp=sharing
- 실제 시연 사진 https://drive.google.com/file/d/1-uCUjCN65ohan37IZXuJfmotn8XtTQRB/view?usp=sharing


# 가상 피팅 & 나만의 옷장 서비스
# AI 기반 가상 피팅 및 맞춤형 옷장 관리 서비스

본 프로젝트는 AI와 컴퓨터 비전 기술을 활용한 혁신적인 옷장 관리 웹사이트를 제안합니다.
- AR(증강현실)과 생성형 신경망을 통해 구현된 가상 피팅 기능을 중심으로, 사용자들은 온라인 상에서도 간편하고 효과적으로 의류를 관리하고 코디네이션 할 수 있습니다.
- 장고(Django) 프레임워크를 기반으로 개발된 본 웹사이트는 인공지능 모델과의 유연한 호환을 이룹니다. 
- 개인화된 데이터베이스를 이용해 간편하게 의류를 관리할 수 있습니다.

# 기대효과
- 전세계적으로 인기를 끌고 있는 K-드라마와 연계하여 사용자들은 K-패션 및 K-뷰티를 가상으로 체험할 수 있습니다.
- 사용자는 자신의 체형과 취향에 맞는 의상을 가상으로 입어보고, 다양한 스타일을 손쉽게 시도해 볼 수 있습니다.
- 개인의 패션 감각을 향상시키고, 구매 전 의사결정을 돕는 동시에 지속 가능한 패션 소비 문화 형성에 기여하고자 합니다.
- 본 서비스는 AI 기술과 패션 산업의 창의적 융합을 통해 사용자 경험을 한층 더 높이는 혁신적인 솔루션이 될 것입니다.

- 최종 버전은 branch master
## 메인 화면
![메인화면](https://github.com/hs-grad-2023/django/assets/121769819/99698443-b4fc-437f-9eb5-497ac08fcc07)
- ### 로그인 시
![로그인시 메인화면](https://github.com/hs-grad-2023/django/assets/121769819/9c37d1da-5c81-4d10-aa6e-36303701a67d)
## 날씨api를 기반으로 챗gpt를 활용한 코디 추천
![날씨와 코디 추천](https://github.com/hs-grad-2023/django/assets/121769819/1590726e-e503-4e91-9e9d-5de5a61fb9f3)
- ### 코디 추천
![코디추천](https://github.com/hs-grad-2023/django/assets/121769819/a7f5d64e-415b-455a-8aa1-2eab78fbad5c)

## 회원 가입
![회원가입](https://github.com/hs-grad-2023/django/assets/121769819/f1ac4268-0be8-493c-a745-db9d5b81c3b1)
- ### 회원 가입 성공 시
![회원가입성공](https://github.com/hs-grad-2023/django/assets/121769819/14877b6e-db1d-415f-b8cb-60e0f4af4a83)
## 마이 페이지
![마이 페이지](https://github.com/hs-grad-2023/django/assets/121769819/bc09f1eb-daec-472d-ad61-afed04ea3396)

## 코디북
- ### 사용자 선호 스타일 선택
![코디북 설정](https://github.com/hs-grad-2023/django/assets/121769819/0ea03363-2f73-4914-a7c9-9204d501481b)
- ### 사용자 선호 스타일을 기반으로 한 무신사 코디북 불러오기
![코디북 설정후 코디추천](https://github.com/hs-grad-2023/django/assets/121769819/efbf6206-3a7c-4d16-8e78-a2c57b512910)
## 내 옷장
- ### 옷장 업로드
![옷장 업로드](https://github.com/hs-grad-2023/django/assets/121769819/d476d09d-d9c8-412c-90d9-4f6af3d9946e)
- ### 내 옷장
![내 옷장](https://github.com/hs-grad-2023/django/assets/121769819/f250002d-3f87-40a4-8af0-f840b2b8fbe0)
- ### 내 옷 상세 보기
![내 옷 상세 보기](https://github.com/hs-grad-2023/django/assets/121769819/3202df02-9c1e-4664-abc2-3bb4ced50cad)
## 옷 자랑 커뮤니티
![옷 자랑 커뮤니티](https://github.com/hs-grad-2023/django/assets/121769819/ba79e3d6-a896-4659-9ad4-e8e613bcd75c)
- ### 상세 페이지
![옷 자랑 커뮤니티 상세](https://github.com/hs-grad-2023/django/assets/121769819/b73322d9-9791-4c1e-a9c0-f70f24209356)
## 가상 피팅
- ### 가상 피팅 메뉴
![가상 피팅 메뉴](https://github.com/hs-grad-2023/django/assets/121769819/2e47653d-13bf-42dd-b0ee-1597e6ad5525)
- ### 웹캠을 이용한 실시간 가상 피팅
    - ### 가상 피팅 옷장
      ![가상 피팅 옷장](https://github.com/hs-grad-2023/django/assets/121769819/05102643-b967-4140-b850-2dc47dc7d2ef)
      - ### 인공지능 SAM(Segment Anything Model)을 이용한 옷 분리
        ![옷 누끼](https://github.com/hs-grad-2023/django/assets/121769819/e1928538-3245-4745-95cf-8dd46770b81c)
        - User Interface를 이용하여 홈페이지에서도 구동 가능하도록 구현
      - ### 옷장 넣기 완료
        ![옷장 넣기 완료](https://github.com/hs-grad-2023/django/assets/121769819/35bd02c0-becc-4129-813b-fb481d974dfb)
      - ### 옷장 결과
        ![누끼 결과](https://github.com/hs-grad-2023/django/assets/121769819/c0608b09-9bc4-4d34-a6c8-ede922cb172c)
        - Openpose를 이용하여 x,y 좌표값에 따라서 옷 사이즈 맞춤 변경
    - ### 웹캠 가상 피팅
      ![가상피팅](https://github.com/hs-grad-2023/django/assets/121769819/fd59589b-73a8-4cda-865e-e6a0e5c5d105)
      - ### 사진 찍기
      ![사진찍기](https://github.com/hs-grad-2023/django/assets/121769819/9cf2cb35-546f-4f28-8352-bb7ce246209b)
- ### 사진으로 가상 피팅
    - ### 모델 고르기
      ![가상피팅 사진으로](https://github.com/hs-grad-2023/django/assets/121769819/80ef1777-98f7-4b1d-9d1b-326fd7d65c79)
    - ### 옷 고르기
      ![사진옷 고르기](https://github.com/hs-grad-2023/django/assets/121769819/059d59b4-289a-4414-9644-58d6d6735e7f)
    - ### 결과(VTON 인공지능 모델 이용)
      ![사진 결과](https://github.com/hs-grad-2023/django/assets/121769819/0fb52826-a959-4580-b27b-7e3d574e8d37)
      - 사진은 저장하여 개인 맞춤형 옷장으로 따로 관리 가능


- ## 웹사이트 플로우 차트
    - ![flowchart](https://github.com/user-attachments/assets/cf77aa47-fa99-4a7a-865d-b31326c6963a)
















