# SWMaestro 10기 "돌아가는 세상" Django 서버 코드

### Set up

```python
cd /path/to/p1040_chatbot

virtualenv venv

source /path/to/p1040_chatbot/venv/bin/activate

pip install -r requirements.txt

cd /path/to/p1040_chatbot/hoxymetoo

mkdir static

vim key.py # 보안을 위해 직접 관리

#################### key.py #######################
  # mysql_conf = {
  #    'ENGINE': 'django.db.backends.mysql',
  #    'NAME': '',
  #    'USER': '',
  #    'PASSWORD': '',
  #    'HOST': '',
  #    'PORT': '3306',
  #    'OPTIONS': {
  #        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
  #    },
  # }
  # aes_key = ''
###################################################

python /path/to/p1040_chatbot/manage.py collectstatic

sudo systemctl restart httpd

# wget https://hoxymetoo.com/create-disable
```



### Database EER Image

<img src="./images/EER.svg" width="90%"></img>