"""
프로그램 ID:SV-1910-PY
프로그램명:urls.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-08-16
버전:0.5
설명:
- Django 서버에서 어떤 url이 어떤 view를 담당할 것인가에 대한 파일이다.
"""

"""hoxymetoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from hoxymetoo import settings
from addresses.views import SiDoViewSet, SiGunGuViewSet, AddressViewSet
from members.views import MemberViewSet
from welfares.views import WelfareViewSet, IndexViewSet, WelfareIndexViewSet, create_disable_data_in_database
from qnas.views import CategoryViewSet, QuestionViewSet, AnswerViewSet, QnaViewSet
from chatbot.views import ChatBotViewSet
from receivableMoney.views import MemberReceivableMoneyViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('sido', SiDoViewSet, basename="sido")
router.register('sigungu', SiGunGuViewSet, basename="sigungu")
router.register('address', AddressViewSet, basename="address")
router.register('members', MemberViewSet, basename="members")
router.register('welfares', WelfareViewSet, basename="welfares")
router.register('indexes', IndexViewSet, basename="indexes")
router.register('welindexes', WelfareIndexViewSet, basename="welindexes")
router.register('categories', CategoryViewSet, basename="categories")
router.register('questions', QuestionViewSet, basename="questions")
router.register('answers', AnswerViewSet, basename="answers")
router.register('qnas', QnaViewSet, basename="qnas")
router.register('chatlogs', ChatBotViewSet, basename="chatlogs")
router.register('receivablemoney', MemberReceivableMoneyViewSet, basename="receivablemoney")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('create-disable/', create_disable_data_in_database)
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
