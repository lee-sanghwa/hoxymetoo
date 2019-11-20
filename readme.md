# SWMaestro 10기 "돌아가는 세상" Django 서버 코드

### Set up

```python
cd /path/to/hoxymetoo

virtualenv venv

source /path/to/hoxymetoo/venv/bin/activate

pip install -r requirements.txt

cd /path/to/hoxymetoo/hoxymetoo

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
  # aes_key = 'weAreTeamOfTurningWorld!10'
###################################################

python /path/to/hoxymetoo/manage.py collectstatic

sudo systemctl restart httpd

# wget https://hoxymetoo.com/create-disable
```

