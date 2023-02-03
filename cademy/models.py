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
    name = models.CharField(max_length=64, verbose_name='基金名称', db_index=True, )
    process = models.IntegerField(choices=PROCESS, default=1)


class MathCademy(models.Model):
    category = models.IntegerField(choices=Cademy.CATEGORY, default=1)
