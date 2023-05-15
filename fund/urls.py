from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from douyin.views import DouYinUserViewSet
from fund.views import FundExpenseViewSet
from sentry_performance.views import SentryUserViewSet
from utools.views import UToolsViewSet

router = routers.DefaultRouter()
router.trailing_slash = '/?'

router.register(r'(?P<version>(v4))/douyin/users', DouYinUserViewSet, )
router.register(r'(?P<version>(v4))/fund_expense', FundExpenseViewSet, )
router.register(r'(?P<version>(v4))/sentry', SentryUserViewSet, basename='sentry')
router.register(r'(?P<version>(v4))/utools', UToolsViewSet, basename='utools')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
]
