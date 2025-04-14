from django.db import models


class Cademy(models.Model):
    CATEGORY = (
        (1, '数学类'),
        (2, '工具类'),
        (3, '网络安全'),
        (4, '前端'),
        (5, '快速构建网站'),
        (6, 'Python'),
    )
    PROCESS = (
        (1, '未开始学习'),
        (2, '学习中'),
        (3, '学习完成'),
    )
    name = models.CharField(verbose_name='网站名称', max_length=64, default='', )
    host = models.CharField(verbose_name='网站地址', max_length=200, default='')
    process = models.IntegerField(verbose_name='进度', choices=PROCESS, default=1)
    remark = models.TextField(verbose_name='描述', max_length=2048, default='')
    category = models.IntegerField(choices=CATEGORY, default=1, verbose_name='类别')
    every_day = models.BooleanField(default=False, verbose_name='每日了解')

    class Meta:
        verbose_name_plural = '学院'
