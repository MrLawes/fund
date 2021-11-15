from django.db import models


class Fund(models.Model):
    name = models.CharField(max_length=64, verbose_name='基金名称', db_index=True, )
    code = models.CharField(max_length=64, verbose_name='代码', db_index=True, )
    three_yearly_change = models.IntegerField(verbose_name='三年年化', default=0)
    space_expense = models.IntegerField(verbose_name='单份投入金额', default=0)
    from_value = models.FloatField(verbose_name='从该市值开始', default=0)
    to_value = models.FloatField(verbose_name='到该市值结束', default=0)
    fee = models.FloatField(verbose_name='买入费率 %', default=0)

    class Meta:
        verbose_name_plural = '基金'

    def __str__(self):
        return self.name

    @property
    def day_change(self):
        """ 天化 """
        return (1 + (self.three_yearly_change / 100.0)) ** (1.0 / (3 * 12 * 30)) - 1

    @property
    def pyramid_stage(self):
        """ 金字塔阶段 """
        max_value = max(self.from_value, self.to_value)
        min_value = min(self.from_value, self.to_value)
        half = min_value + (max_value - min_value) / 2
        stage_value = (self.to_value - half) / 10
        stage = [half + stage_value * i for i in range(0, 11)]
        if self.from_value < self.to_value:
            stage = stage[::-1]
        return stage


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
    # todo 刷数据
    expense = models.FloatField(verbose_name='确认金额', default=0)
    hold = models.FloatField(verbose_name='确认份额', default=0)

    class Meta:
        verbose_name_plural = '基金购买记录'

    @classmethod
    def get_hold(self, fund_value, expense, fee):
        """ 计算持有份数
        :param: expense:        确认金额
        :param: fund_value:     单位净值
        """
        expense -= expense * fee / 100
        # 持有份数 = 确认金额 / 单位净值
        return round(expense / fund_value, 2)

    @property
    def fund_value(self):
        return FundValue.objects.get(fund=self.fund, deal_at=self.deal_at)
