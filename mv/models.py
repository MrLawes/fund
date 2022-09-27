from django.contrib.auth.models import User
from django.db import models


# https://www.bilibili.com/video/BV1F64y1u7SQ?p=3
class Mv(models.Model):
    download_url = models.CharField(verbose_name='下载地址', max_length=1024)
    # 需要下载 -》下载中 -》下载完成修改文件名 -》下载完成
    action = models.CharField(verbose_name='行为', default='需要下载', max_length=200)
    name = models.CharField(verbose_name='文件名字', default='', null=True, max_length=400)

# for i in range(1, 22):
#     Mv.objects.get_or_create(download_url=f'https://www.bilibili.com/video/BV1F64y1u7SQ?{i}')
