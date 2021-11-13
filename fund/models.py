from django.db import models


# Create your models here.


class Fund(models.Model):
    name = models.CharField(max_length=64, verbose_name='基金名称', db_index=True, )
    code = models.CharField(max_length=64, verbose_name='代码', db_index=True, )
    three_yearly_change = models.IntegerField(max_length=64, verbose_name='三年年化', db_index=True, default=0)

    def __str__(self):
        return self.name


class FundValue(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    deal_at = models.DateField(verbose_name='交易时间', db_index=True, )
    value = models.FloatField(verbose_name='单位净值', db_index=True, )
    rate = models.FloatField(verbose_name='日增长率', db_index=True, )
