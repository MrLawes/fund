from django.contrib.auth.models import User
from django.db import models


class DouYinUser(User):
    # username: 抖音号码；first_name: 抖音名
    fens_count = models.IntegerField(verbose_name='粉丝数量', default=0)
