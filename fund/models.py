from django.db import models


class Fund(models.Model):
    name = models.CharField(max_length=64, verbose_name='基金名称', db_index=True, )
    code = models.CharField(max_length=64, verbose_name='代码', db_index=True, )
    three_yearly_change = models.IntegerField(verbose_name='三年年化', default=0)
    space_expense = models.IntegerField(verbose_name='总仓位的55份投入金额', default=0)
    from_value = models.FloatField(verbose_name='从该市值开始', default=0)
    to_value = models.FloatField(verbose_name='到该市值结束', default=0)

    class Meta:
        verbose_name_plural = '基金'

    def __str__(self):
        return self.name

    @property
    def day_change(self):
        """ 天化 """
        return (1 + (self.three_yearly_change / 100.0)) ** (1.0 / (3 * 12 * 30)) - 1

    @property
    def total_space_expense(self):
        """ 总仓位金额 """
        return self.space_expense * 55


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
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, verbose_name='基金名称', )
    deal_at = models.DateField(verbose_name='发布日期', db_index=True, )
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
