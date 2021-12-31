import datetime

from django import forms
from django.contrib import admin
from django.utils.html import format_html

from fund.models import Fund, FundValue, FundExpense, FundHoldings


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_html', 'rate', 'expense', 'value',)
    search_fields = ['name', ]
    list_filter = ('name', 'high_sale_low_buy',)

    def get_queryset(self, request):
        return super().get_queryset(request=request).order_by('-newest_rate')

    def expense(self, obj):
        expense = FundExpense.objects.filter(fund=obj, expense_type='buy').values_list('expense', flat=True, )
        return round(sum(expense), 2)

    expense.short_description = '已投入资金'

    def name_html(self, obj):
        return format_html(f'<a href="/admin/fund/fundexpense/?fund__name={obj.name}" target="_blank">{obj.name}</a>')

    name_html.short_description = '基金名称'

    def rate(self, obj):
        fund_value = FundValue.objects.filter(fund=obj).order_by('deal_at').last()
        if not fund_value:
            return 0
        rate = fund_value.rate
        if rate > 0:
            rate = f"""<span style="color: red;">{rate}</span>"""
        else:
            rate = f"""<span style="color: green;">{rate}</span>"""
        return format_html(f"({str(fund_value.deal_at)[5:]}) {rate}　　　")

    rate.short_description = '估算涨幅'

    def value(self, obj):
        hold = sum(FundExpense.objects.filter(fund=obj, expense_type='buy').values_list('hold', flat=True))
        fund_value = FundValue.objects.filter(fund=obj, ).order_by('deal_at').last()
        if not fund_value:
            return '0'
        hope_value = 0
        for fund_expense in FundExpense.objects.filter(fund=obj, expense_type='buy'):
            hope_value += fund_expense.hope_value
        if hold * fund_value.value > hope_value:
            result = f"""<span style="color: red;">{(hold * fund_value.value):0.02f}</span>"""
        else:
            result = f"""<span style="color: green;">{(hold * fund_value.value):0.02f}</span>"""
        return format_html(f"""{result}/{hope_value:0.02f}　　　　　""")

    value.short_description = '金额/止赢金额✌️'

    # def pyramid(self, obj):
    #     if obj.high_sale_low_buy:
    #         return ''
    #
    #     fund_value = FundValue.objects.filter(fund=obj, ).order_by('deal_at').last()
    #     当前净值_index = None
    #     html_list = []
    #     for index, stage in enumerate(obj.pyramid_stage):
    #
    #         if obj.from_value > obj.to_value:
    #             if fund_value.value > stage and 当前净值_index is None:
    #                 rate = (stage - fund_value.value) * 100 / fund_value.value
    #                 html_list.append(f"当前净值: {fund_value.value:.4f}；下阶段 ⬇️ 涨幅:{rate:.2f}%　　　　　</br>")
    #                 当前净值_index = len(html_list)
    #
    #         elif obj.from_value < obj.to_value:
    #             if fund_value.value > stage and 当前净值_index is None:
    #                 rate = (fund_value.value - stage) * 100 / fund_value.value
    #                 html_list.append(f"当前净值: {fund_value.value:.4f}；下阶段 ⬆️ 涨幅:{rate:.2f}%　　　　　　　　　　　</br>")
    #                 当前净值_index = len(html_list)
    #
    #         html_list.append(
    #             f"{index:02} 仓位: 市值: {stage:.4f}；总投入: {5000 + ((1 + index) * index / 2 * obj.space_expense)}　　　　　　</br>")
    #
    #     if obj.from_value < obj.to_value and 当前净值_index is None:
    #         rate = (stage - fund_value.value) * 100 / fund_value.value
    #         html_list.append(f"当前净值: {fund_value.value:.4f}；下阶段 ⬆️ 涨幅:{rate:.2f}%　　　　　　　　　　　</br>")
    #         当前净值_index = len(html_list)
    #
    #     if 当前净值_index is None:
    #         当前净值_index = 0
    #     html_slice_start = 当前净值_index - 3
    #     html_slice_start = 0 if html_slice_start < 0 else html_slice_start
    #     html_slice_end = 当前净值_index + 2
    #     html_list = html_list[html_slice_start:html_slice_end]
    #
    #
    #     return format_html(''.join(html_list))
    #
    # pyramid.short_description = '金字塔'


@admin.register(FundValue)
class FundValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'fund', 'deal_at', 'value', 'rate',)
    search_fields = ['fund__name', 'deal_at', ]
    list_filter = ('fund__name',)

    def get_queryset(self, request):
        result = super().get_queryset(request=request).order_by('-deal_at', )
        return result


class FundExpenseForm(forms.ModelForm):
    class Meta:
        model = FundExpense
        fields = "__all__"

    def clean(self):
        fund_value = FundValue.objects.get(fund=self.cleaned_data['fund'], deal_at=self.cleaned_data['deal_at'])
        # 买入费率
        fee = self.cleaned_data['fund'].fee
        # 扣除买入费率，计算出购买份额
        total_expense = self.cleaned_data['expense']
        total_hold = FundExpense.get_hold(fund_value=fund_value.value, expense=total_expense, fee=fee)
        split_hold = self.cleaned_data.get('split_hold', 0)
        if split_hold:  # 如果需要拆分
            # 创建一份拆分后的交易记录
            split_expense = round(self.cleaned_data['expense'] * split_hold / total_hold, 2)
            self.cleaned_data['split_hold'] = 0
            self.cleaned_data['expense'] = split_expense
            self.cleaned_data['hold'] = split_hold
            FundExpense.objects.create(**self.cleaned_data)
            # 修改原交易数据
            self.cleaned_data['expense'] = round(total_expense - split_expense, 2)
            self.cleaned_data['hold'] = round(total_hold - split_hold, 2)
        else:  # 不拆分，记录下总的份额
            self.cleaned_data['hold'] = total_hold
        return self.cleaned_data


@admin.register(FundExpense)
class FundExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'deal_at', 'transaction_rule', 'fund', 'hold', 'expense', 'hold_value', 'hold_rate_persent', 'hope_value',
        'can_sale_hold', 'sale_using_date',)
    search_fields = ['fund__name', 'id', ]
    list_filter = ('fund__name', 'fund__high_sale_low_buy')
    actions = ['sum_hold', ]
    form = FundExpenseForm

    def get_queryset(self, request):
        results = super().get_queryset(request=request)
        for result in results:
            last_fundvalue = FundValue.objects.filter(fund=result.fund_value.fund).order_by('deal_at').last()
            value = result.hold * last_fundvalue.value
            result.hold_rate = (((value - result.expense) / result.expense) * 100)
            if result.sale_using_date and datetime.datetime.now().date() > result.sale_using_date:
                result.sale_using_date = None
            result.save()
        results = super().get_queryset(request=request).order_by('-hold_rate')
        return results

    def sum_hold(self, request, queryset):
        hold = sum(queryset.values_list('hold', flat=True))
        self.message_user(request, f"共计 {hold:0.02f} 份")

    sum_hold.short_description = "计算份数"

    def hold_value(self, obj):
        last_fundvalue = FundValue.objects.filter(fund=obj.fund_value.fund).order_by('deal_at').last()
        value = round(obj.hold * last_fundvalue.value, 2)
        hope_value = obj.hope_value
        if hope_value > value:
            color = 'green'
        else:
            color = 'red'

        return format_html(f'<span style="color: {color};">{value}</span>')

    hold_value.short_description = '持有市值'

    def hold_rate_persent(self, obj):
        last_fundvalue = FundValue.objects.filter(fund=obj.fund_value.fund).order_by('deal_at').last()
        value = obj.hold * last_fundvalue.value
        return f"{(((value - obj.expense) / obj.expense) * 100):0.02f}%"

    hold_rate_persent.short_description = '持有收益率'

    def hope_value(self, obj):
        return obj.hope_value

    hope_value.short_description = '期望市值'

    def transaction_rule(self, obj):
        return obj.fund.transaction_rule

    transaction_rule.short_description = '交易规则'

    def can_sale_hold(self, obj):
        """ 获得最佳可售份额 """

        fund = obj.fund
        # 最优出售天数, 一般短线 7 天，长线 30 天。
        best_transaction_rule_days = fund.best_transaction_rule_days

        # 最优出售日期，一般短线为 7 天后免手续费
        best_rule_date = datetime.datetime.now() - datetime.timedelta(days=best_transaction_rule_days + 1)

        hold = sum(list(
            FundExpense.objects.filter(fund=obj.fund, expense_type='buy', deal_at__lt=best_rule_date).values_list(
                'hold', flat=True)))

        # todo hold - 近 天数内出售的部分
        return f"{hold:0.02f}"

    can_sale_hold.short_description = '可售份额'


@admin.register(FundHoldings)
class FundHoldingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'catetory_name', 'expense', 'persent')

    def persent(self, obj):
        result = obj.expense * 100 / max(list(FundHoldings.objects.values_list('expense', flat=True)))
        return f"{result:0.02f}%"

    persent.short_description = '仓位占比'
