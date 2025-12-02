from django.db import models
from django.utils import timezone


class Fund(models.Model):
    FUND_CATEGORY = (
        (1, '医疗'),
        (2, '白酒'),
        (3, '半导体'),
        (4, '军工'),
        (5, '新能源'),
        (6, '黄金'),
        (7, '债券'),
    )
    category = models.IntegerField(choices=FUND_CATEGORY, default=0)
    name = models.CharField(max_length=64, verbose_name='基金名称', db_index=True, )
    code = models.CharField(max_length=64, verbose_name='代码', db_index=True, )
    fee = models.FloatField(verbose_name='买入费率 %', default=0)
    newest_rate = models.FloatField(verbose_name='最新估算涨幅', default=0, null=True)
    high_sale_low_buy = models.BooleanField(verbose_name='高抛低吸', default=False, )
    is_advance = models.BooleanField(verbose_name='是否是进阶理财', default=True, )

    class Meta:
        verbose_name_plural = '基金'

    def __str__(self):
        return self.name


class FundValue(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, verbose_name='基金名称')
    deal_at = models.DateField(verbose_name='发布日期', db_index=True, )
    value = models.FloatField(verbose_name='单位净值', )
    rate = models.FloatField(verbose_name='日增长率', default=0)

    class Meta:
        unique_together = ('fund', 'deal_at',)
        verbose_name_plural = '基金净值'

    def __str__(self):
        return f"{self.fund.name} {self.deal_at} {self.value=}"


class FundExpense(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, verbose_name='基金名称', )
    deal_at = models.DateField(verbose_name='交易日期', db_index=True, )
    expense = models.FloatField(verbose_name='确认金额', default=0)
    hold = models.FloatField(verbose_name='确认份额', default=0)
    hold_rate = models.FloatField(verbose_name='持有收益率', default=0)
    expense_type = models.CharField(verbose_name='基金交易类型: buy: 购买；sale：出售', max_length=8, default='buy')
    split_hold = models.FloatField(verbose_name='拆分份额', default=0)
    sale_at = models.DateField(verbose_name='出售日期', default=None, null=True, blank=True, )
    need_buy_again = models.BooleanField(verbose_name='卖出去过的', default=False)  # todo 改名 is_sale
    newest_value = models.FloatField(verbose_name='最新单位净值', default=0)
    annual_interest_rate = models.DecimalField(
        verbose_name='投资回报年化率%', default=0, decimal_places=2, max_digits=10
    )

    class Meta:
        verbose_name_plural = '基金购买记录'

    def set_annual_interest_rate(self):
        """ 更新投资回报年化率 """

        # 增值部分
        appreciation = self.newest_value * self.hold - self.expense
        days = (timezone.localtime().date() - self.deal_at).days
        if days > 0:
            self.annual_interest_rate = (appreciation / days / self.expense) * 356 * 100
            self.save(update_fields=['annual_interest_rate', ])

    @classmethod
    def get_hold(cls, fund_value, expense, fee):
        """ 计算持有份数
        :param: expense:        确认金额
        :param: fund_value:     单位净值
        """
        expense -= expense * fee / 100
        # 持有份数 = 确认金额 / 单位净值
        return round(expense / fund_value, 2)  # noqa

    @property
    def fund_value(self):
        return FundValue.objects.get(fund=self.fund, deal_at=self.deal_at)  # noqa


class FundHoldings(models.Model):
    catetory_name = models.CharField(verbose_name='分类', max_length=64, )
    expense = models.FloatField(verbose_name='确认金额', default=0)
    hold = models.FloatField(verbose_name='持有份额', default=0)

    class Meta:
        verbose_name_plural = '基金仓位'
