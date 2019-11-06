"""
프로그램 ID:SV-1000-PY
프로그램명:models.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-08-16
버전:0.5
설명:
- ERD를 통해 데이터베이스 스크립트를 생성하여 실제 데이터베이스에 만들어진 테이블들과 연동하기위한 것으로, 회원관련 내용을 다루고 있다.
"""

from django.db import models
from welfares.models import Disable, Welfare, LifeCycle, TargetCharacter, Desire, HouseType
from addresses.models import Address


# 데이터베이스의 가족 테이블과 연동하기 위한 클래스
class Family(models.Model):
    familyId = models.AutoField(
        primary_key=True,
        db_column='familyid'
    )
    # 가족 구성원의 생일 (20190807)
    familyBirth = models.CharField(
        max_length=8,
        db_column='familybirth'
    )
    # 가족 구성원의 성별 (1: 남성, 2: 여성)
    familyGender = models.IntegerField(
        db_column='familygender'
    )
    # https 통신으로 회원 정보에 접근했을 때 가족 구성원에 대한 정보를 주기위한 테이블 (20190807-1)
    familyInfo = models.CharField(
        max_length=20,
        db_column='familyinfo'
    )
    familyAddressId = models.ForeignKey(
        Address,
        null=True,
        on_delete=models.CASCADE,
        db_column='familyaddressid'
    )

    class Meta:
        # 가족 테이블의 이름을 Family로 설정 (원래는 members_Family)
        db_table = 'Family'


# 데이터베이스의 직업 테이블과 연동하기 위한 클래스
class Job(models.Model):
    jobId = models.AutoField(
        primary_key=True,
        # jobId의 이름을 jobid로 설정 (원래는 jobId)
        db_column='jobid'
    )
    # 직업 이름
    jobName = models.CharField(
        max_length=127,
        unique=True,
        # jobName의 이름을 jobname로 설정 (원래는 jobName)
        db_column='jobname'
    )

    class Meta:
        # 직업 테이블의 이름을 Job으로 설정 (원래는 members_Job)
        db_table = 'Job'


# 데이터베이스의 회원 테이블과 연동하기 위한 클래스
class Member(models.Model):
    # 회원의 Social ID (facebook_test000000001)
    socialId = models.CharField(
        max_length=255,
        primary_key=True,
        db_column='socialid'
    )
    # 회원의 push token ID (push_test000000001)
    pushToken = models.CharField(
        max_length=255,
        null=True,
        db_column='pushtoken'
    )
    # 회원의 social id에 대한 SHA-256 해쉬 값 (e0d3b72f72183185c11356d4f280ceceb336622fbab3B4f4fbe6af73ca4dbcbc)
    memKey = models.CharField(
        max_length=255,
        unique=True,
        db_column='memkey'
    )
    # 회원의 email 주소 (test000000001@test.com)
    memEmail = models.CharField(
        max_length=511,
        null=True,
        db_column='email'
    )
    # 회원의 비밀번호 (123456) -> 확장서을 위해서 생성
    memPassword = models.CharField(
        max_length=127,
        null=True,
        db_column='password'
    )
    memReceivableMoney = models.IntegerField(
        default=0,
        db_column='receivablemoney'
    )
    memReceivableMoneyDescribe = models.TextField(
        null=True,
        db_column='receivablemoneydescribe'
    )
    # 회원의 생일 (20190807)
    memBirthday = models.CharField(
        max_length=63,
        null=True,
        db_column='st_birthday'
    )
    # 회원의 성별 (1: 남성, 2: 여성)
    memGender = models.CharField(
        max_length=63,
        null=True,
        db_column='st_gender'
    )
    # 회원의 가족 구성원 수 (5)
    memFamily = models.CharField(
        max_length=63,
        null=True,
        db_column='st_family'
    )
    # 회원의 소득분위 (0: 차상위 계층)
    memIncome = models.CharField(
        max_length=63,
        null=True,
        db_column='st_income'
    )
    # 회원의 보훈 여부 (0: 비대상(기본 값), 1: 대상)
    memBohun = models.CharField(
        max_length=63,
        null=True,
        db_column='st_bohun'
    )
    memAddressId = models.OneToOneField(
        Address,
        null=True,
        on_delete=models.CASCADE,
        db_column='memaddressid'
    )
    # 회원 정보 생성 일자 + 시간 (20190723215934: 2019년 07월 23알 21시 59분 34초)
    createDateTime = models.CharField(
        max_length=14,
        db_column='createdatetime'
    )
    # 회원 정보 생성 일자 (20190723: 2019년 07월 23알)
    createDate = models.CharField(
        max_length=8,
        db_column='createdate'
    )
    # 회원 정보 생성 시간 (215934: 21시 59분 34초)
    createTime = models.CharField(
        max_length=6,
        db_column='createtime'
    )
    # 회원 정보 수정 일자 + 시간 (20190723215934: 2019년 07월 23알 21시 59분 34초)
    updateDateTime = models.CharField(
        max_length=14,
        db_column='updatedatetime'
    )
    # 회원 정보 수정 일자 (20190723: 2019년 07월 23알)
    updateDate = models.CharField(
        max_length=8,
        db_column='updatedate'
    )
    # 회원 정보 수정 시간 (215934: 21시 59분 34초)
    updateTime = models.CharField(
        max_length=6,
        db_column='updatetime'
    )
    # 회원의 가족구성원들
    families = models.ManyToManyField(
        Family,
        through='MemFamily'
    )
    # 회원이 갖고 있는 직업들
    jobs = models.ManyToManyField(
        Job,
        through='MemJob'
    )
    # 회원이 받을 수 있는 복지들
    welfares = models.ManyToManyField(
        Welfare,
        through='MemWelfare'
    )
    # 회원의 대상특성들
    targetCharacters = models.ManyToManyField(
        TargetCharacter,
        through='MemTargetCharacter'
    )
    # 회원의 생애주기들
    lifeCycles = models.ManyToManyField(
        LifeCycle,
        through='MemLifeCycle'
    )

    # 회원이 관심있어하는 분야들
    desires = models.ManyToManyField(
        Desire,
        through='MemDesire'
    )
    # 회원의 가구유형들
    houseTypes = models.ManyToManyField(
        HouseType,
        through='MemHouseType'
    )
    # 회원이 갖고 있는 질병들
    disables = models.ManyToManyField(
        Disable,
        through='MemDisable'
    )

    class Meta:
        # 회원 테이블의 이름을 Member로 설정 (원래는 members_Member)
        db_table = 'Member'


# 데이터베이스의 회원과 가족 구성원 테이블을 연결한 테이블과 연동하기 위한 클래스
class MemFamily(models.Model):
    memFamilyId = models.AutoField(
        primary_key=True,
        db_column='memfamilyid'
    )
    socialId = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='socialid'
    )
    familyId = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        db_column='familyid'
    )

    class Meta:
        db_table = 'Memfamily'


# 데이터베이스의 회원과 직업 테이블을 연결한 테이블과 연동하기 위한 클래스
class MemJob(models.Model):
    memJobId = models.AutoField(
        primary_key=True,
        db_column='memjobid'
    )
    socialId = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='socialid'
    )
    jobId = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        db_column='jobid'
    )

    class Meta:
        db_table = 'Memjob'


# 데이터베이스의 회원과 복지 테이블을 연결한 테이블과 연동하기 위한 클래스
class MemWelfare(models.Model):
    memWelfareId = models.AutoField(
        primary_key=True,
        db_column='memwelfareid'
    )
    socialId = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='socialid'
    )
    welId = models.ForeignKey(
        Welfare,
        on_delete=models.CASCADE,
        db_column='welid'
    )
    createDateTime = models.CharField(
        max_length=14,
        db_column='createdatetime'
    )
    createDate = models.CharField(
        max_length=8,
        db_column='createdate'
    )
    createTime = models.CharField(
        max_length=6,
        db_column='createtime'
    )

    class Meta:
        db_table = 'Memwelfare'


# 데이터베이스의 회원과 대상특성 테이블을 연결한 테이블과 연동하기 위한 클래스
class MemTargetCharacter(models.Model):
    memTargetCharacterId = models.AutoField(
        primary_key=True,
        db_column='memtargetcharacterid'
    )
    socialId = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='socialid'
    )
    targetCharacterId = models.ForeignKey(
        TargetCharacter,
        on_delete=models.CASCADE,
        db_column='targetcharacterid'
    )

    class Meta:
        db_table = 'Memtargetcharacter'


# 데이터베이스의 회원과 생애주기 테이블을 연결한 테이블과 연동하기 위한 클래스
class MemLifeCycle(models.Model):
    memLifeCycleId = models.AutoField(
        primary_key=True,
        db_column='memlifecycleid'
    )
    socialId = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='socialid'
    )
    lifeCycleId = models.ForeignKey(
        LifeCycle,
        on_delete=models.CASCADE,
        db_column='lifecycleid'
    )

    class Meta:
        db_table = 'Memlifecycle'


# 데이터베이스의 회원과 욕구 테이블을 연결한 테이블과 연동하기 위한 클래스
class MemDesire(models.Model):
    memDesireId = models.AutoField(
        primary_key=True,
        db_column='memdesireid'
    )
    socialId = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='socialid'
    )
    desireId = models.ForeignKey(
        Desire,
        on_delete=models.CASCADE,
        db_column='desireid'
    )

    class Meta:
        db_table = 'Memdesire'


# 데이터베이스의 회원과 가구유형 테이블을 연결한 테이블과 연동하기 위한 클래스
class MemHouseType(models.Model):
    memHouseTypeId = models.AutoField(
        primary_key=True,
        db_column='memhousetypeid'
    )
    socialId = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='socialid'
    )
    houseTypeId = models.ForeignKey(
        HouseType,
        on_delete=models.CASCADE,
        db_column='housetypeid'
    )

    class Meta:
        db_table = 'Memhousetype'


# 데이터베이스의 회원과 질병 테이블을 연결한 테이블과 연동하기 위한 클래스
class MemDisable(models.Model):
    memDisableId = models.AutoField(
        primary_key=True,
        db_column='memdisableid'
    )
    socialId = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='socialid'
    )
    disableId = models.ForeignKey(
        Disable,
        on_delete=models.CASCADE,
        db_column='disableid'
    )

    class Meta:
        db_table = 'Memdisable'


class Feedback(models.Model):
    FeedbackId = models.AutoField(
        primary_key=True,
        db_column='feedback_id'
    )
    MemberEmail = models.CharField(
        max_length=511,
        db_column='member_email',
        null=True
    )
    MemberKey = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='member_key',
        db_constraint='fk_feedback_member_key',
        null=True
    )
    MemberPhone = models.CharField(
        max_length=30,
        db_column='member_phone',
        null=True
    )
    FeedbackContent = models.TextField(
        db_column='feedback_content'
    )
    CreateColumn = models.DateTimeField(
        db_column='create_column'
    )
    UpdateColumn = models.DateTimeField(
        db_column='update_column'
    )

    class Meta:
        db_table = 'Feedback'
