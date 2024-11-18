from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # username：用户名
    # email: 电子邮件
    # password：密码
    # first_name：名
    # last_name：姓
    # is_active: 是否为活跃用户。默认是True
    # is_staff: 是否为员工。默认是False
    # is_superuser: 是否为管理员。默认是False
    # date_joined: 加入日期。系统自动生成。
    id=models.BigAutoField(primary_key=True)
    last_login=models.DateTimeField(db_comment='上次登录时间',null=True)
    is_superuser=models.BooleanField(default=False)
    access_system_a = models.BooleanField(default=False)
    access_system_b = models.BooleanField(default=False)
    access_system_c = models.BooleanField(default=False)
    access_system_d = models.BooleanField(default=False)
    access_system_e = models.BooleanField(default=False)
    access_system_f = models.BooleanField(default=False)
    access_system_g = models.BooleanField(default=False)
    access_system_h = models.BooleanField(default=False)

