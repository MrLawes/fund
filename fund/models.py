from django.db import models

# Create your models here.



class Fund(models.Model):

    name = models.CharField(max_length=64, verbose_name='基金名称', db_index=True, )
    code  = models.CharField(max_length=64, verbose_name='代码', db_index=True, )
