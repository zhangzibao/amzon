from django.db import models

from datetime import datetime
from foods.models import Foods
from django.contrib.auth import get_user_model

User = get_user_model()

my_status = (
    (0, "正常"),
    (1, "禁用"),
    (2, "删除"),
)


class order(models.Model):
    ORDER_STATUS = (
        (0, "未接单"),
        (1, "已接单"),
        (2, "已配餐"),
        (3, "已取餐"),
        (4, "已评价"),
    )
    PAY_TYPE = (
        ("alipay", "支付宝"),
        ("wechat", "微信"),
    )
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="商家Id", related_name="o_sid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户Id", related_name="o_uid")
    order_sn = models.CharField("订单编号", max_length=30, null=True, blank=True, unique=True)
    post_script = models.CharField("订单留言", max_length=200, null=True)
    pay_price = models.DecimalField("订单金额", max_digits=10, decimal_places=2, default=0)
    status = models.IntegerField("记录状态", default=0, choices=my_status)
    add_time = models.DateTimeField("添加时间", default=datetime.now)
    order_status = models.SmallIntegerField("订单状态", choices=ORDER_STATUS, default=1)

    # # 微信支付会用到
    # nonce_str = models.CharField("随机加密串", max_length=50, null=True, blank=True, unique=True)
    # # 支付宝交易号
    # trade_no = models.CharField("交易号", max_length=100, unique=True, null=True, blank=True)
    # # 支付状态

    # # 订单的支付类型
    # pay_type = models.CharField("支付类型", choices=PAY_TYPE, default="alipay", max_length=10)
    # receive_time = models.DateTimeField("接单时间", default=None)
    class Meta:
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class order_foods(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE, verbose_name="订单id", related_name="o_id")
    foods = models.ForeignKey(Foods, on_delete=models.CASCADE, verbose_name="商品id", related_name="o_food")
    num = models.IntegerField("数量", default=1)

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)


class shopcart(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="商家id", related_name="s_seller")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户id", related_name="user_id")
    status = models.SmallIntegerField("记录状态", default=0, choices=my_status)
    foods = models.ForeignKey(Foods, on_delete=models.CASCADE, verbose_name="商品", related_name="s_food")
    nums = models.IntegerField("购买数量", default=0)
    add_time = models.DateTimeField("添加时间", default=datetime.now)
    update_time = models.DateTimeField("更新时间", default=datetime.now)

    class Meta:
        verbose_name = '购物车喵'
        verbose_name_plural = verbose_name
        unique_together = ("seller", "user", "foods")

    def __str__(self):
        return "%s(%d)".format(self.foods.name, self.nums)

#
# class shopcart_foods(models.Model):
#     shopcart = models.ForeignKey(shopcart, on_delete=models.CASCADE, verbose_name="购物车id", related_name="sc_id")
#     foods = models.ForeignKey(Foods, on_delete=models.CASCADE, verbose_name="商品id", related_name="s_food")
#     foods_price = models.DecimalField("单个价格", max_digits=10, decimal_places=2)
#     num = models.IntegerField("数量", default=1)
#     status = models.SmallIntegerField("记录状态", default=0, choices=my_status)
#
#     class Meta:
#         verbose_name = "订单商品"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return str(self.shopcart.id)
#
# class cashbook(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="商家Id")
