from django.db import models
# Create your models here.
from django.db import models


class big_kind(models.Model):
    name = models.CharField("大类名", max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        ordering = ('created',)
        db_table = 'big_kind'


class small_kind(models.Model):
    big = models.ForeignKey(big_kind, on_delete=models.CASCADE, verbose_name="大类Id", related_name="big_id")
    name = models.CharField("小类名", max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        ordering = ('created',)
        db_table = 'small_kind'


class tiny_kind(models.Model):
    small = models.ForeignKey(small_kind, on_delete=models.CASCADE, verbose_name="小类Id", related_name="small_id")
    name = models.CharField("具体类名", max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        ordering = ('created',)
        db_table = 'tiny_kind'


class goods(models.Model):
    tiny = models.ForeignKey(tiny_kind, on_delete=models.CASCADE, verbose_name="具体类Id", related_name="tiny_id")
    name = models.CharField("商品名", max_length=255, blank=True)
    url = models.CharField("链接", max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        ordering = ('created',)
        db_table = 'goods'


# 代理ip
class ProxyIp(models.Model):
    ip = models.CharField("ip地址", max_length=50)
    port = models.CharField("端口号", max_length=10)
    speed = models.IntegerField("网速")
    proxy_type = models.CharField("代理类型", max_length=10, default='HTTP')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        ordering = ('created',)
        db_table = 'proxy_ip'


class amazon_goods(models.Model):
    name = models.CharField("商品名称", max_length=255, blank=True, default="无")
    price = models.CharField("商品价格", max_length=255, blank=True, default="无")
    goal_price = models.CharField("商品预期价格", max_length=255, blank=True, default="0")
    url = models.CharField("商品url", max_length=255, blank=True, default="无")
    imgurl = models.CharField("商品图片url", max_length=255, blank=True, default="无")
    # 0 未发送消息，1 已发送消息
    status = models.SmallIntegerField(default=0, verbose_name="记录状态")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        managed = True
        unique_together = ('name',)
        db_table = 'amazon_goods'
