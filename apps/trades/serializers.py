# trade/serializer.py
__author__ = 'derek'

import time

from .models import shopcart
from rest_framework import serializers
from foods.models import Foods
from .models import order, order_foods
from amazon.settings import ali_pub_key_path, private_key_path
from utils.alipay import AliPay
from django.contrib.auth import get_user_model

User = get_user_model()


class FoodsSerializer(serializers.ModelSerializer):
    # 覆盖外键字段
    # ratings = ratingSerializer()
    # nums = serializers.SerializerMethodField()
    class Meta:
        model = Foods
        fields = '__all__'


class ShopCartDetailSerializer(serializers.ModelSerializer):
    '''
    购物车商品详情信息
    '''
    # 一个购物车对应一个商品
    foods = FoodsSerializer(many=False, read_only=True)

    class Meta:
        model = shopcart
        fields = ("foods", "nums", "seller")


class ShopCartSerializer(serializers.Serializer):
    # 获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField()
    # 这里是继承Serializer，必须指定queryset对象，如果继承ModelSerializer则不需要指定
    # foods是一个外键，可以通过这方法获取foods object中所有的值
    foods = serializers.PrimaryKeyRelatedField(required=True, queryset=Foods.objects.all())
    seller = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())

    # 继承的Serializer没有save功能，必须写一个create方法
    def create(self, validated_data):
        # validated_data是已经处理过的数据
        # 获取当前用户
        # view中:self.request.user；serizlizer中:self.context["request"].user
        user = self.context["request"].user
        nums = validated_data["nums"]
        foods = validated_data["foods"]

        existed = shopcart.objects.filter(user=user, foods=foods)
        # 如果购物车中有记录，数量+1
        # 如果购物车车没有记录，就创建
        if existed:
            existed = existed[0]
            existed.nums += nums
            if existed.nums <= 0:
                existed.delete()
            else:
                existed.save()
        else:
            # 添加到购物车
            existed = shopcart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


# 订单中的商品
class order_foodsSerialzier(serializers.ModelSerializer):
    foods = FoodsSerializer(many=False)

    class Meta:
        model = order_foods
        fields = "__all__"


# 订单商品信息
# foods字段需要嵌套一个order_foodsSerializer
class OrderDetailSerializer(serializers.ModelSerializer):
    o_id = order_foodsSerialzier(many=True)
    class Meta:
        model = order
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # 生成订单的时候这些不用post
    status = serializers.IntegerField(read_only=True)
    # trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    # nonce_str = serializers.CharField(read_only=True)
    # pay_type = serializers.CharField(read_only=True)
    order_status = serializers.IntegerField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)

    # seller = serializers.IntegerField(read_only=True)

    def generate_order_sn(self):
        # 生成订单号
        # 当前时间+userid+随机数
        from random import Random
        # print(self.context["request"].user.id)
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        # validate中添加order_sn，然后在view中就可以save
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = order
        fields = "__all__"
