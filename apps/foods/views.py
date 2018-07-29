from django.shortcuts import render

# Create your views here.
# googd/views.py
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from foods.serializers import FoodsSerializer, KindSerializer, MySerializer
from .models import Kinds, Ratings, Foods
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class FoodsPagination(PageNumberPagination):
    '''
    商品列表自定义分页
    '''
    # 默认每页显示的个数
    page_size = 12
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 100


class FoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品列表，分页，搜索，过滤，排序
    retrieve:
        获取商品详情
    '''
    # authentication_classes = (TokenAuthentication,)
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    # 这里必须要定义一个默认的排序,否则会报错
    queryset = Foods.objects.all().order_by('id')
    # 分页
    pagination_class = FoodsPagination
    # 序列化
    serializer_class = FoodsSerializer


class KindListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品列表，分页，搜索，过滤，排序
    retrieve:
        获取商品详情
    '''
    # authentication_classes = (TokenAuthentication,)
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    # 这里必须要定义一个默认的排序,否则会报错
    queryset = Kinds.objects.all().order_by('id')
    # 序列化
    serializer_class = KindSerializer


class MyListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                    viewsets.GenericViewSet, mixins.DestroyModelMixin):
    '''
    list:
        商品列表，分页，搜索，过滤，排序
    retrieve:
        获取商品详情
    '''
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    # 这里必须要定义一个默认的排序,否则会报错
    # queryset = Kinds.objects.all().order_by('id')
    # 序列化
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = MySerializer

    def get_queryset(self):
        return Kinds.objects.all()

    def perform_create(self, serializer):
        return None


