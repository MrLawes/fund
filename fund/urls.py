from django.contrib import admin
from django.urls import path

# from rest_framework import routers

# from fund.views import FundViewSet

# router = routers.DefaultRouter()
# router.trailing_slash = '/?'
#
# router.register(r'(?P<version>(v4))/fund', FundViewSet, base_name='fund')

urlpatterns = [
    path('admin/', admin.site.urls),
]
