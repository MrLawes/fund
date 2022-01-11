import datetime

from django.db import models


class Fund(models.Model):
    name = models.CharField(max_length=64, verbose_name='基金名称', db_index=True, )
    code = models.CharField(max_length=64, verbose_name='代码', db_index=True, )
    three_yearly_change = models.IntegerField(verbose_name='三年年化', default=0)
    space_expense = models.IntegerField(verbose_name='单份投入金额', default=0)
    from_value = models.FloatField(verbose_name='从该单位净值开始', default=0)
    to_value = models.FloatField(verbose_name='到该单位净值结束', default=0)
    fee = models.FloatField(verbose_name='买入费率 %', default=0)
    newest_rate = models.FloatField(verbose_name='最新估算涨幅', default=0, null=True)
    transaction_rule = models.CharField(max_length=64, verbose_name='交易规则', default='', )
    high_sale_low_buy = models.BooleanField(verbose_name='高抛低吸', default=False, )
    best_transaction_rule_days = models.IntegerField(verbose_name='最优出售天数', default=30)

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
        # half = min_value + (max_value - min_value) / 2
        stage_value = (max_value - min_value) / 10
        stage = [min_value + stage_value * i for i in range(0, 11)]
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
    deal_at = models.DateField(verbose_name='交易日期', db_index=True, )
    expense = models.FloatField(verbose_name='确认金额', default=0)
    hold = models.FloatField(verbose_name='确认份额', default=0)
    hold_rate = models.FloatField(verbose_name='持有收益率', default=0)
    sale_using_date = models.DateField(verbose_name='可售恢复时间', default=None, null=True, blank=True, )  # todo delete
    expense_type = models.CharField(verbose_name='基金交易类型: buy: 购买；sale：出售', max_length=8, default='buy')
    split_hold = models.FloatField(verbose_name='拆分份额', default=0)
    sale_at = models.DateField(verbose_name='出售日期', default=None, null=True, blank=True, )
    is_buy_again = models.BooleanField(verbose_name='是否已经回购', default=False)
    headimg = models.FileField(upload_to="img/", default='')

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

    @property
    def hope_value(self):
        # 天化
        day_change = self.fund_value.fund.day_change
        # 持有时间
        days = datetime.datetime.now().date() - self.fund_value.deal_at
        days = days.days
        # 通过天化得期望市值，再加上手续费
        value = ((1 + day_change) ** days) * self.expense
        value *= 1.0065
        return round(value, 2)


class FundHoldings(models.Model):
    catetory_name = models.CharField(verbose_name='分类', max_length=64, )
    expense = models.FloatField(verbose_name='确认金额', default=0)

    class Meta:
        verbose_name_plural = '基金仓位'

#
# class FundFee(models.Model):
#     fund = models.ForeignKey(Fund, on_delete=models.CASCADE, verbose_name='基金名称', )
#     day = models.IntegerField(verbose_name='天数', )
#     fee = models.FloatField(verbose_name='手续费%')
#
#     class Meta:
#         verbose_name_plural = '基金手续费配置'
