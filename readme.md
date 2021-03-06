# SWMaestro 10기 "돌아가는 세상" Django 서버 코드

## 1. 개요

<img src="./images/SW_ad_front.jpeg"></img>
* * *
<img src="./images/SW_ad_back.jpeg"></img>

* * *

## 2. aws 구성

<img src="./images/aws.png"></img>

* * *

## 3. 환경 설정


##### 깃에서 프로젝트를 다운받은 후 프로젝트 폴더로 이동
```
cd /path/to/p1040_chatbot
```

* * *

##### 파이썬 프로젝트들 끼리의 패키 버전 충돌을 방지하기위해 가상의 파이썬 환경을 설정
```
virtualenv venv
```

* * *


##### 가상환경의 파이썬으로 환경변수를 일시적으로 변경
```
source /path/to/p1040_chatbot/venv/bin/activate
```

* * *

##### 프로젝트를 실행하는데에 필요한 패키지들을 설치
```
pip install -r requirements.txt
```

* * *

##### 프로젝트 내부의 hoxymetoo 폴더로 이동
```
cd /path/to/p1040_chatbot/hoxymetoo
```

* * *

##### 아파치에서 각종 css파일등을 찾을 수 있도록하기 위해 설정
```
mkdir static
cd /path/to/p1040_chatbot

python manage.py collectstatic
```

* * *

##### 보안을 위해 key들은 직접 관리 (db연결 환경설정 & db 암호화에대한 키 값) 
```
vim key.py

--------------in key.py------------

mysql_conf = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': '데이터베이스 이름',
    'USER': '데이터베이스 유저',
    'PASSWORD': '유저의 비밀번호',
    'HOST': '서버 주소',
    'PORT': '3306',
    'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    },
}

aes_key = ''
###################################################
```

* * *

##### 서버 작동
```
sudo systemctl restart httpd
```

##### disable에 대한 데이터들을 넣기 위해 아래의 주소로 요청

```
wget https://hoxymetoo.com/create-disable
```

* * *

## 4. Database EER Image

<img src="./images/EER.svg"></img>

* * *

## 5. 대표적인 기능 (복지 추천 서비스)

#### 설명
1. 앱에서 사용자를 등록하거나 수정을 하기위해 HTTP METHOD 중 POST나 PATCH를 사용하여 서버에 요청을 보낸다. 
2. 받은 값을 토대로 개인특성, 가정환경, 관심분야, 나이대별에 맞는 복지를 찾는다.
3. 제일 많이 중복되는 복지 순으로 앱으로 전송한다.
* * *

<img src="./images/recom_wel.png"></img>

* * *

## 6. 실제 예시

아래는 현재 개발되어있는 api에 대한 목록입니다.

사진을 클릭하시면 api를 직접 확인하실 수 있습니다.

현재 앱에서 이 api를 사용중이므로 실제 데이터를 삭제하시거나 변경하지 말아주시기 바랍니다.

[![api 루트로 이동](./images/api.png)](https://hoxymetoo.com/api)

* * *
