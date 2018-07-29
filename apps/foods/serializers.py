# goods/serializers.py

from rest_framework import serializers
from .models import Foods, Ratings, Kinds
from django.db.models import Q
from trades.serializers import ShopCartDetailSerializer
from trades.models import shopcart


class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kinds
        fields = "__all__"


class ratingSerializer(serializers.ModelSerializer):
    '''热搜'''

    class Meta:
        model = Ratings
        fields = "__all__"


# 商品列表页


class MySerializer(serializers.ModelSerializer):
    foods = serializers.SerializerMethodField()

    class Meta:
        model = Kinds
        fields = ('name', 'type', 'foods')

    def get_foods(self, obj):
        # 将这个商品相关父类子类等都可以进行匹配
        # all_goods = Foods.objects.filter(Q())

        all_foods = Foods.objects.filter(Q(kinds=obj.id))
        foods_serializer = TruFSerializer(all_foods, many=True, context={'request': self.context['request']})
        # print(serializers.HiddenField(default=serializers.CurrentUserDefault()))
        return foods_serializer.data


class FoodsSerializer(serializers.ModelSerializer):
    # 覆盖外键字段
    # ratings = ratingSerializer()
    # nums = serializers.SerializerMethodField()
    class Meta:
        model = Foods
        fields = '__all__'


class TruFSerializer(serializers.ModelSerializer):
    # ratings = ratingSerializer()
    nums = serializers.SerializerMethodField()

    class Meta:
        model = Foods
        fields = '__all__'

    #
    def get_nums(self, obj):
        # 将这个商品相关父类子类等都可以进行匹配
        # all_goods = Foods.objects.filter(Q())
        all_foods = shopcart.objects.filter(foods=obj.id, user=self.context["request"].user.id).values('nums')
        if all_foods:
            # print(all_foods[0])
            return all_foods[0]['nums']
        else:
            return 0
# foods_serializer = ShopCartDetailSerializer(all_foods, many=True, context={'request': self.context['request']})
# data = foods_serializer.data
# print(vars(data))
# return foods_serializer.data
