from django.contrib.auth.models import User
from django.db import models


class DouYinUser(User):
    # username: 抖音号码；first_name: 抖音名
    fens_count = models.IntegerField(verbose_name='粉丝数量', default=0)
    follow_count = models.IntegerField(verbose_name='关注数量', default=0)
    relationship = models.CharField(max_length=32, verbose_name='关系', default='')
    href = models.URLField(max_length=200, verbose_name='链接', default='')
    create_at = models.DateTimeField(verbose_name="关注时间", auto_now_add=True)

    class Meta:
        verbose_name_plural = '抖音用户'
