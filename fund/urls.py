from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from douyin.views import DouYinUserViewSet

router = routers.DefaultRouter()
router.trailing_slash = '/?'

router.register(r'(?P<version>(v4))/douyin/users', DouYinUserViewSet, )

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
]
