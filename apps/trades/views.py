# trade/views.py
import json
from django.http import JsonResponse, QueryDict
from django.views.generic import View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from .serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderDetailSerializer, FoodsSerializer, \
    OrderSerializer
from .models import shopcart, order_foods, order
from rest_framework import mixins
from django.shortcuts import render, redirect

from datetime import datetime
from utils.alipay import AliPay
from rest_framework.views import APIView
from amazon.settings import ali_pub_key_path, private_key_path
from rest_framework.response import Response


class shopcartViewset(viewsets.ModelViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create：
        加入购物车
    delete：
        删除购物记录
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCartSerializer
    # 商品的id
    lookup_field = "s_food"

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    # 获取购物车列表
    def get_queryset(self):
        return shopcart.objects.filter(user=self.request.user)


class OrderViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   viewsets.GenericViewSet, mixins.DestroyModelMixin):
    """
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create：
        新增订单
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    # 动态配置serializer
    def get_serializer_class(self):
        if self.action == "list":
            return OrderDetailSerializer

        else:
            return OrderSerializer

    # 获取订单列表
    def get_queryset(self):
        return order.objects.filter(user=self.request.user)

    # 在订单提交保存之前还需要多两步步骤，所以这里自定义perform_create方法
    # 1.将购物车中的商品保存到order_goods中6+
    # 2.情况购物车
    def perform_create(self, serializer):
        order = serializer.save()
        # 获取购物车所有商品
        shop_carts = shopcart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = order_foods()
            order_goods.foods = shop_cart.foods
            order_goods.num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            # 清空购物车
            shop_cart.delete()
        print('我', order, 'ddd')
        return order


class AlipayView(APIView):

    def post(self, request):
        # 存放post里面所有的数据
        processed_dict = {}
        # 取出post里面的数据
        for key, value in request.POST.items():
            processed_dict[key] = value
        # 把signpop掉，文档有说明
        sign = processed_dict.pop("sign", None)

        # 进行验证
        # verify_re = alipay.verify(processed_dict, sign)
        verify_re = True
        # 如果验签成功
        if verify_re is True:
            # 商户网站唯一订单号
            order_sn = processed_dict.get('out_trade_no', None)

            # 查询数据库中订单记录
            existed_orders = order.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                # 订单商品项
                order_goods = existed_order.goods.all()
                # 商品销量增加订单中数值
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                # 更新订单状态
                existed_order.pay_time = datetime.now()
                existed_order.save()
            # 需要返回一个'success'给支付宝，如果不返回，支付宝会一直发送订单支付成功的消息
            return Response("success")


class TodoItemView(View):
    def get(self, request):
        # json_data = json.loads(request.body)
        # json_data = {'status': 1}
        # todo = order.objects.get(id=1)
        # todo.order_status = json_data['status']
        # todo.save()
        # response = JsonResponse({'result': 'success'})
        # response['Access-Control-Allow-Origin'] = '*'
        return Response("success")

    def put(self, request):
        json_data = json.loads(request.body)
        todo = order.objects.get(id=json_data['id'])
        todo.order_status = json_data['status']
        todo.save()
        resp = JsonResponse({'result': 'success'})
        resp['Access-Control-Allow-Origin'] = '*'
        return resp

    def post(self, request):
        json_data = json.loads(request.body)
        todo = order.objects.get(id=json_data['id'])
        todo.delete()
        response = JsonResponse({'result': 'success'})
        response['Access-Control-Allow-Origin'] = '*'
        return response
