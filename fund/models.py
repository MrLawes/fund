from django.db import models


# Create your models here.


class Fund(models.Model):
    name = models.CharField(max_length=64, verbose_name='基金名称', db_index=True, )
    code = models.CharField(max_length=64, verbose_name='代码', db_index=True, )
    three_yearly_change = models.IntegerField(verbose_name='三年年化', default=0)

    class Meta:
        verbose_name_plural = '基金'

    def __str__(self):
        return self.name


class FundValue(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, verbose_name='基金名称')
    deal_at = models.DateField(verbose_name='发布日期', db_index=True, )
    value = models.FloatField(verbose_name='单位净值', )
    rate = models.FloatField(verbose_name='日增长率', )

    class Meta:
        unique_together = ('fund', 'deal_at',)
        verbose_name_plural = '基金净值'

    def __str__(self):
        return f"{self.fund.name} {self.deal_at}"


class FundExpense(models.Model):
    fund_value = models.OneToOneField(FundValue, on_delete=models.CASCADE, verbose_name='基金市值', unique=True)
    # todo 刷数据
    expense = models.FloatField(verbose_name='确认金额', default=0)
    hold = models.FloatField(verbose_name='持有份数', default=0)

    class Meta:
        verbose_name_plural = '基金购买记录'

    @classmethod
    def get_hold(self, fund_value, expense):
        """ 计算持有份数
        :param: expense:        确认金额
        :param: fund_value:     单位净值
        """

        # 持有份数 = 确认金额 / 单位净值
        return round(expense / fund_value, 2)
