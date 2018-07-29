from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django.http import JsonResponse
from spiders.serializers import goodSerializer
from .models import amazon_goods
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from users.models import news
from users.serializers import newsSerializer
import json


class MyListViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品列表，分页，搜索，过滤，排序
    retrieve:
        获取商品详情
    '''
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    # 序列化
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = goodSerializer

    def put(self, request, *args, **kwargs):
        # print(self.request.data)
        try:
            good = amazon_goods.objects.get(name=self.request.data['name'])
        except amazon_goods.DoesNotExist:
            # 捕获City不存在的异常, 抛出异常或是自己处理
            return None
        good.status = 0
        good.goal_price = self.request.data['goal_price']
        good.save()
        response = JsonResponse({'result': 'success'})
        response['Access-Control-Allow-Origin'] = '*'
        return response

    def get_queryset(self):
        return amazon_goods.objects.all()


class newsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品列表，分页，搜索，过滤，排序
    retrieve:
        获取商品详情
    '''
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    # 序列化
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = newsSerializer

    def get_queryset(self):
        return news.objects.all()
