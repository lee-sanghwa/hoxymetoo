"""
프로그램 ID:SV-1100-PY
프로그램명:models.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-08-16
버전:0.5
설명:
- ERD를 통해 데이터베이스 스크립트를 생성하여 실제 데이터베이스에 만들어진 테이블들과 연동하기위한 것으로, 복지관련 내용을 다루고 있다.
"""

from django.db import models
from addresses.models import Address


# 장애 등급
class DisableLevel(models.Model):
    # 1, 2, 3, 4, 5, 6
    disableLevelId = models.AutoField(
        primary_key=True,
        db_column='disablelevelid'
    )
    # 1급, 2급, 3급, 4급, 5급, 6급
    disableLevelName = models.CharField(
        max_length=127,
        unique=True,
        db_column='disablelevelname'
    )

    class Meta:
        # 장애 등급 테이블의 이름을 DisableLevel 설정 (원래는 welfares_DisableLevel)
        db_table = 'Disablelevel'


# 장애 유형
class DisableType(models.Model):
    # 10, 20, 30, 40, 50, 60, 70, 80, 90, A0, B0, C0, D0, E0, F0
    disableTypeId = models.CharField(
        max_length=2,
        primary_key=True,
        db_column='disabletypeid'
    )
    # 지체, 시각, 청각, 언어, 지적, 뇌병변, 자폐성, 정신, 신장, 심장, 호흡기, 간, 안면, 장루, 간질
    disableTypeName = models.CharField(
        max_length=127,
        unique=True,
        db_column='disabletypename'
    )

    class Meta:
        # 장애 유형 테이블의 이름을 Disabletype 설정 (원래는 welfares_DisableType)
        db_table = 'Disabletype'


# 장애 유형 + 장애 등급 테이블
class Disable(models.Model):
    disableId = models.AutoField(
        primary_key=True,
        db_column='disableid'
    )
    disableLevelId = models.ForeignKey(
        DisableLevel,
        on_delete=models.CASCADE,
        db_column='disablelevelid'
    )
    disableTypeId = models.ForeignKey(
        DisableType,
        on_delete=models.CASCADE,
        db_column='disabletypeid'
    )
    # 지체 1급
    disableName = models.CharField(
        max_length=255,
        unique=True,
        db_column='disablename'
    )

    class Meta:
        # 장애 테이블의 이름을 Disable 설정 (원래는 welfares_Disable)
        db_table = 'Disable'


# 가구 유형
class HouseType(models.Model):
    # 001 ~ 007
    houseTypeId = models.CharField(
        primary_key=True,
        max_length=3,
        db_column='housetypeid'
    )
    # 해당없음, 한부모, 다문화, 조손, 새터민,소년소녀가장, 독거노인
    houseTypeName = models.CharField(
        unique=True,
        max_length=127,
        db_column='housetypename'
    )

    class Meta:
        # 가구 유형 테이블의 이름을 Housetype 설정 (원래는 welfares_HouseType)
        db_table = 'Housetype'


# 욕구
class Desire(models.Model):
    # 0000000, 1000000, ...... , A000000
    desireId = models.CharField(
        primary_key=True,
        max_length=7,
        db_column='desireid'
    )
    # 안전, 건강, 일상생활유지 , 가족관계, 사회적 관계, 경제, 교육, 고용, 생활환경, 법률 및 권익보장, 기타
    desireName = models.CharField(
        unique=True,
        max_length=127,
        db_column='desirename'
    )

    class Meta:
        # 욕구 테이블의 이름을 Desire 설정 (원래는 welfares_Desire)
        db_table = 'Desire'


# 생애주기
class LifeCycle(models.Model):
    # 001 ~ 006
    lifeCycleId = models.CharField(
        primary_key=True,
        max_length=6,
        db_column='lifecycleid'
    )
    # 영유아, 아동, 청소년, 청년, 중장년, 노년
    lifeCycleName = models.CharField(
        unique=True,
        max_length=127,
        db_column='lifecyclename'
    )

    class Meta:
        # 생애주기 테이블의 이름을 Lifecycle 설정 (원래는 welfares_LifeCycle)
        db_table = 'Lifecycle'


# 대상특성
class TargetCharacter(models.Model):
    # 001 ~ 006
    targetCharacterId = models.CharField(
        primary_key=True,
        max_length=3,
        db_column='targetcharacterid'
    )
    # 해당없음, 여성, 임산부, 장애, 국가유공자등 보훈대상자, 실업자
    targetCharacterName = models.CharField(
        unique=True,
        max_length=127,
        db_column='targetcharactername'
    )

    class Meta:
        db_table = 'Targetcharacter'


# 소관 조직
class Organization(models.Model):
    # 1, 2, 3, ......
    organizationId = models.AutoField(
        primary_key=True,
        db_column='organizationid'
    )
    # 기초생활보장과
    organizationName = models.CharField(
        unique=True,
        max_length=127,
        db_column='organizationname'
    )

    class Meta:
        db_table = 'Organization'


# 소관 부처
class Ministry(models.Model):
    # 1, 2, 3, ......
    ministryId = models.AutoField(
        primary_key=True,
        db_column='ministryid'
    )
    # 보건복지부
    ministryName = models.CharField(
        unique=True,
        max_length=127,
        db_column='ministryname'
    )

    class Meta:
        db_table = 'Ministry'


# 책임 기관에 대한 테이블
class Responsible(models.Model):
    # 책임 기관 아이디 ( 1 ~ )
    responsibleId = models.AutoField(
        primary_key=True,
        db_column='responsibleid'
    )
    # 소관 조직 아이디 ( 1 ~ )
    organizationId = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        db_column='organizationid'
    )
    # 소관 부처 아이디 ( 1 ~ )
    ministryId = models.ForeignKey(
        Ministry,
        on_delete=models.CASCADE,
        db_column='ministryid'
    )
    # 책임 기관 이름 ( 기초생활보장과-보건복지부 )
    responsibleName = models.CharField(
        unique=True,
        max_length=255,
        db_column='responsiblename'
    )

    class Meta:
        db_table = 'Responsible'


class Index(models.Model):
    indexName = models.CharField(
        primary_key=True,
        max_length=255,
        db_column='indexname'
    )

    class Meta:
        db_table = 'Index'


class Welfare(models.Model):
    # Api에서 제공하는 복지 id ( WII00000141 )
    welId = models.CharField(
        max_length=63,
        primary_key=True,
        db_column='welid'
    )
    # 복지이름 ( (기초생활)생계급여 )
    welName = models.CharField(
        max_length=127,
        blank=True,
        db_column='welname'
    )
    # 복지 요약 ( 생활이 어려운 수급자에게 일상생활에 필요한 급여를 지급하여 최저생활을 보장하고 자활을 조성하는 것을 목적으로 함 )
    welSummary = models.CharField(
        max_length=511,
        null=True,
        blank=True,
        db_column='welsummary'
    )
    # 복지 대상자 상세내용 ( ㅇ 가구의 소득인정액이 생계급여 선정기준 이하로서 생계급여 수급자로 결정된 수급자 - 단, 타 법령에 ......)
    targetDetail = models.TextField(
        null=True,
        blank=True,
        db_column='targetdetail')
    # 선정 기준 ( ㅇ 아래 소득인정액 기준 및 부양의무자 기준을 동시에 충족하여야 함 [소득인정액 기준] ㅇ 기준 중위소득 30% 이하 1인가구 : 512,102원)
    supportStandard = models.TextField(
        null=True,
        blank=True,
        db_column='supportstandard'
    )
    # 복지 혜택 내용 ( ㅇ 아래 소득인정액 기준 및 부양의무자 기준을 동시에 충족하여야 함 [소득인정액 기준] ㅇ 기준 중위소득 30% 이하 1인가구 :
    supportMoney = models.TextField(
        null=True,
        blank=True,
        db_column='supportmoney'
    )
    # 복지 이용 및 신청 방법 ( 1. 초기상담 및 서비스 신청 : 읍/면/동 주민센터 2. 사실조사 및 심사 : 시/군/구청 3. 서비스 결정 : 시/군/구청
    howToApply = models.TextField(
        null=True,
        blank=True,
        db_column='howtoapply'
    )
    # 복지 신청 방법 이미지링크 ( http://www.bokjiro.go.kr/upload_data/AC/service01/WELSVC_201406272206180.gif )
    howToApplyImageLink = models.TextField(
        null=True,
        blank=True,
        db_column='howtoapplyimagelink'
    )
    # 문의처 이름 ( 보건복지상담센터 )
    contactInfoName = models.TextField(
        null=True,
        blank=True,
        db_column='contactinfoname'
    )
    # 문의처 연락처 ( 129 )
    contactInfoNumber = models.TextField(
        null=True,
        blank=True,
        db_column='contactinfonumber'
    )
    # 관련 사이트 이름 ( 보건복지상담센터 )
    siteName = models.TextField(
        null=True,
        blank=True,
        db_column='sitename'
    )
    # 관련 사이트 링크주소 ( http://www.129.go.kr )
    siteLink = models.TextField(
        null=True,
        blank=True,
        db_column='sitelink'
    )
    # 복지 혜택에 필요한 서식/자료 이름 ( 2019년_국민기초생활보장사업안내(최종인쇄).pdf )
    formName = models.TextField(
        null=True,
        blank=True,
        db_column='formname'
    )
    # 복지 혜택에 필요한 서식/자료 링크주소 ( http://www.bokjiro.go.kr/upload_data/AC/service01/WELSVC_201901211704030.pdf )
    formLink = models.TextField(
        null=True,
        blank=True,
        db_column='formlink'
    )
    # 근거 법령 이름 ( 국민기초생활 보장법 )
    lawName = models.TextField(
        null=True,
        blank=True,
        db_column='lawname'
    )
    # 근거 법령 링크주소 ( http://www.law.go.kr/DRF/lawService.do?OC=webmaster&target=law&type=HTML&ID=1973 )
    lawLink = models.TextField(
        null=True,
        blank=True,
        db_column='lawlink'
    )
    # 복지 등록일 ( 2014-07-28 )
    registerDate = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        db_column='registerdate'
    )
    welAddressId = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        db_column='weladdressid'
    )
    # 복지에 해당하는 질병들
    disables = models.ManyToManyField(
        Disable,
        through='WelDisable'
    )
    # 복지와 관련된 가구유형들
    houseTypes = models.ManyToManyField(
        HouseType,
        through='WelHouseType'
    )
    # 복지와 관련된 욕구들
    desires = models.ManyToManyField(
        Desire,
        through='WelDesire'
    )
    # 복지와 관련된 생애주기들
    lifeCycles = models.ManyToManyField(
        LifeCycle,
        through='WelLifeCycle'
    )
    # 복지와 관련된 대상특성들
    targetCharacters = models.ManyToManyField(
        TargetCharacter,
        through='WelTargetCharacter'
    )
    # 복지와 관련된 책임기관들
    responsibles = models.ManyToManyField(
        Responsible,
        through='WelResponsible'
    )
    indexes = models.ManyToManyField(
        Index,
        through='WelIndex'
    )

    class Meta:
        db_table = 'Welfare'


# 데이터베이스의 복지 장애 테이블을 연결한 테이블과 연동하기 위한 클래스
class WelDisable(models.Model):
    welDisableId = models.AutoField(
        primary_key=True,
        db_column='weldisableid'
    )
    welId = models.ForeignKey(
        Welfare,
        on_delete=models.CASCADE,
        db_column='welid'
    )
    disableId = models.ForeignKey(
        Disable,
        on_delete=models.CASCADE,
        db_column='disableid'
    )

    class Meta:
        db_table = 'Weldisable'


# 데이터베이스의 복지와 가구유형 테이블을 연결한 테이블과 연동하기 위한 클래스
class WelHouseType(models.Model):
    welHouseTypeId = models.AutoField(
        primary_key=True,
        db_column='welhousetypeid'
    )
    welId = models.ForeignKey(
        Welfare,
        on_delete=models.CASCADE,
        db_column='welid'
    )
    houseTypeId = models.ForeignKey(
        HouseType,
        on_delete=models.CASCADE,
        db_column='housetypeid'
    )

    class Meta:
        db_table = 'Welhousetype'


# 데이터베이스의 복지와 욕구 테이블을 연결한 테이블과 연동하기 위한 클래스
class WelDesire(models.Model):
    welDesireId = models.AutoField(
        primary_key=True,
        db_column='weldesireid'
    )
    welId = models.ForeignKey(
        Welfare,
        on_delete=models.CASCADE,
        db_column='welid'
    )
    desireId = models.ForeignKey(
        Desire,
        on_delete=models.CASCADE,
        db_column='desireid'
    )

    class Meta:
        db_table = 'Weldesire'


# 데이터베이스의 복지와 생애주기 테이블을 연결한 테이블과 연동하기 위한 클래스
class WelLifeCycle(models.Model):
    welLifeCycleId = models.AutoField(
        primary_key=True,
        db_column='wellifecycleid'
    )
    welId = models.ForeignKey(
        Welfare,
        on_delete=models.CASCADE,
        db_column='welid'
    )
    lifeCycleId = models.ForeignKey(
        LifeCycle,
        on_delete=models.CASCADE,
        db_column='lifecycleid'
    )

    class Meta:
        db_table = 'Wellifecycle'


# 데이터베이스의 복지와 대상특성 테이블을 연결한 테이블과 연동하기 위한 클래스
class WelTargetCharacter(models.Model):
    welTargetCharacterId = models.AutoField(
        primary_key=True,
        db_column='weltargetcharacterid'
    )
    welId = models.ForeignKey(
        Welfare,
        on_delete=models.CASCADE,
        db_column='welid'
    )
    targetCharacterId = models.ForeignKey(
        TargetCharacter,
        on_delete=models.CASCADE,
        db_column='targetcharacterid'
    )

    class Meta:
        db_table = 'Weltargetcharacter'


# 데이터베이스의 복지와 책임기관 테이블을 연결한 테이블과 연동하기 위한 클래스
class WelResponsible(models.Model):
    welResponsibleId = models.AutoField(
        primary_key=True,
        db_column='welresponsibleid'
    )
    welId = models.ForeignKey(
        Welfare,
        on_delete=models.CASCADE,
        db_column='welid'
    )
    responsibleId = models.ForeignKey(
        Responsible,
        on_delete=models.CASCADE,
        db_column='responsibleid'
    )

    class Meta:
        db_table = 'Welresponsible'


class WelIndex(models.Model):
    welIndexId = models.AutoField(
        primary_key=True,
        db_column='welindexid'
    )
    welId = models.ForeignKey(
        Welfare,
        on_delete=models.CASCADE,
        db_column='welid'
    )
    indexName = models.ForeignKey(
        Index,
        on_delete=models.CASCADE,
        db_column='indexname'
    )

    class Meta:
        db_table = 'Welindex'
