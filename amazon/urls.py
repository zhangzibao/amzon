# amazon/urls.py
__author__ = 'derek'

from django.urls import path, include, re_path
import xadmin
from django.views.static import serve
from amazon.settings import MEDIA_ROOT
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from users.views import UserViewset, LoginViewset
from spiders.views import MyListViewSet, newsListViewSet

router = DefaultRouter()

# 配置用户的url
router.register(r'users', UserViewset, base_name="注册接口")
# 商品

router.register(r'goods', MyListViewSet, base_name="商品接口")

router.register(r'news', newsListViewSet, base_name="消息接口")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('ueditor/', include('DjangoUeditor.urls')),
    # 文件
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    # drf文档，title自定义
    path('docs', include_docs_urls(title='超级无敌')),
    # 商品列表页
    re_path('^', include(router.urls)),
    # token
    path('islogin/', views.obtain_auth_token),
    # jwt的认证接口
    path('login/', LoginViewset.as_view()),
    # 配置支付宝支付相关接口的url
    # path('alipay/return/', AlipayView.as_view()),
    # 第三方登录
    path('', include('social_django.urls', namespace='social'))
]
