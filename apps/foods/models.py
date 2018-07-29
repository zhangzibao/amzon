# goods/models.py
__author__ = 'zhangzibao'

from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
GENDER_CHOICES = (
    ("male", u"男"),
    ("female", u"女")
)


class Kinds(models.Model):
    """
    商品分类
    """
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="商家id", related_name="所属商家")
    name = models.CharField('分类名称', default="", max_length=30, help_text="类别名")
    type = models.SmallIntegerField('暂时不知', default=-1)
    add_time = models.DateTimeField("添加时间", default=datetime.now)
    update_time = models.DateTimeField("更新时间", default=datetime.now)

    class Meta:
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name


class Foods(models.Model):
    kinds = models.ForeignKey(Kinds, on_delete=models.CASCADE, verbose_name='所属分类', related_name='foods')
    rating = models.IntegerField("好评率", default=0)
    name = models.CharField("商品名", max_length=50)
    sellCount = models.IntegerField("商品销售量", default=0)
    oldPrice = models.IntegerField("市场价格", default=0)
    price = models.IntegerField("本店价格", default=0)
    description = models.TextField("商品类别描述", max_length=140)
    info = models.TextField("商品简短描述", max_length=140)
    # 首页中展示的商品封面图
    # image = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="大图")
    # icon = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="小图")
    image = models.TextField(null=True, blank=True, verbose_name="大图")
    icon = models.TextField(null=True, blank=True, verbose_name="小图")
    add_time = models.DateTimeField("添加时间", default=datetime.now)
    update_time = models.DateTimeField("更新时间", default=datetime.now)

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Ratings(models.Model):
    text = models.TextField("评论内容", max_length=140)
    avatar = models.ImageField(upload_to="goods/images/", null=True, blank=True, verbose_name="小图")
    rateType = models.IntegerField("不明", default=0)
    rateTime = models.DateTimeField("添加时间", default=datetime.now)
    score = models.IntegerField("评价星数", default=0)
    recommend = models.CharField("评论者id", max_length=100, )
    foods = models.ForeignKey(Foods, on_delete=models.CASCADE, verbose_name="商品id")
    uid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="评论者id", related_name="uid")

    class Meta:
        verbose_name = '评论信息'
        verbose_name_plural = verbose_name
