from django.db import models


class Cademy(models.Model):
    class Meta:
        """ meta """
        abstract = True

    CATEGORY = (
        (1, '数学'),
    )
    PROCESS = (
        (1, '未开始学习'),
        (2, '学习中'),
        (3, '学习完成'),
    )
    name = models.CharField(verbose_name='网站名称', max_length=64, default='', )
    host = models.CharField(verbose_name='网站地址', max_length=200, default='')
    process = models.IntegerField(verbose_name='进度', choices=PROCESS, default=1)


class MathCademy(Cademy):
    category = models.IntegerField(choices=Cademy.CATEGORY, default=1)

    class Meta:
        verbose_name_plural = '数学'
