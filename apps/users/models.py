# users/models.py
__author__ = 'derek'

from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from spiders.models import amazon_goods


class UserProfile(AbstractUser):
    """
    用户信息
    """
    USER_TYPE_LIST = (
        (0, 'user'),
        (1, 'seller'),
    )
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女")
    )
    # 用户用手机注册，所以姓名，生日和邮箱可以为空
    name = models.CharField("姓名", max_length=30, null=True, blank=True)
    birthday = models.DateField("出生年月", null=True, blank=True)
    gender = models.CharField("性别", max_length=6, choices=GENDER_CHOICES, default="female")
    mobile = models.CharField("电话", max_length=11, null=True, blank=True, help_text='手机号')
    email = models.EmailField("邮箱", max_length=100, null=True, blank=True)
    isseller = models.IntegerField("是否是商家用户", choices=USER_TYPE_LIST, default=0)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    验证码
    """
    code = models.CharField("验证码", max_length=10)
    mobile = models.CharField("电话", max_length=11)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "短信验证"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class news(models.Model):
    content = models.TextField(max_length=255, verbose_name="消息内容", default="无")
    good = models.ForeignKey(amazon_goods, on_delete=models.CASCADE, verbose_name="指向商品的外键", related_name="good_id")
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "通知消息"
        verbose_name_plural = verbose_name
