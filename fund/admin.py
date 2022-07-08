import datetime

from django import forms
from django.contrib import admin
from django.db import transaction
from django.utils.html import format_html

from fund.models import Fund, FundValue, FundExpense, FundHoldings


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_html', 'rate', 'expense', 'value', 'hold',)
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

    def hold(self, obj):
        buy_hold = sum(FundExpense.objects.filter(fund=obj, expense_type='buy').values_list('hold', flat=True))
        sale_hold = sum(FundExpense.objects.filter(fund=obj, expense_type='sale').values_list('hold', flat=True))
        return round(buy_hold - sale_hold, 2)

    hold.short_description = '持有份额'

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
        'id', 'deal_at', 'transaction_rule', 'fund_name', 'hold', 'expense', 'hold_value', 'hold_rate_persent',
        'hope_value', 'can_sale_hold', 'buttons',)
    search_fields = ['fund__name', 'id', ]
    list_filter = ('fund__name', 'fund__high_sale_low_buy')
    actions = ['sum_hold', 'sale', ]
    form = FundExpenseForm

    def get_queryset(self, request):
        results = super().get_queryset(request=request)
        for result in results:
            last_fundvalue = FundValue.objects.filter(fund=result.fund_value.fund).order_by('deal_at').last()
            value = result.hold * last_fundvalue.value
            # 卖出去过的，不展示持有收益率
            if result.need_buy_again:
                result.hold_rate = 0
            else:
                result.hold_rate = (((value - result.expense) / result.expense) * 100)
            result.save()
        results = super().get_queryset(request=request).order_by('-hold_rate')
        return results

    def fund_name(self, obj):
        if obj.expense_type == 'buy':
            result = f'<a href="/admin/fund/fundexpense/?fund__name={obj.fund.name}" target="_blank">{obj.fund.name}</a>'
        elif obj.expense_type == 'sale':
            result = f"""<span style="text-decoration: line-through">{obj.fund.name}</span>"""
        return format_html(result)

    fund_name.short_description = "基金名称"

    def buttons(self, obj):

        result = ''
        if obj.expense_type == 'buy':

            if obj.need_buy_again:
                return f"""已出售"""

            if obj.is_buy_again:  # todo delete
                result = '已回购'
            else:
                if obj.need_buy_again:
                    result = f"""已出售"""
                else:
                    result = f"""<a href="/v4/fund_expense/{obj.id}/sale/">出售</a>"""

        return format_html(result)

    buttons.short_description = "操作"

    def sum_hold(self, request, queryset):
        hold_buy = sum(queryset.filter(expense_type='buy').values_list('hold', flat=True))
        hold_sale = sum(queryset.filter(expense_type='sale').values_list('hold', flat=True))
        self.message_user(request, f"共计 {(hold_buy - hold_sale):0.02f} 份")

    sum_hold.short_description = "计算份数"

    def sale(self, request, queryset):

        with transaction.atomic():
            if queryset.filter(expense_type='sale').exists():
                self.message_user(request, "存在已售")
            elif len(list(queryset.values_list('fund', flat=True))) != 1:
                self.message_user(request, "只能出售同类基金")
            elif queryset.filter(need_buy_again='True').exists():
                self.message_user(request, "存在需要回购的份额，不可以出售")
            else:
                fund = queryset.filter(expense_type='buy').first().fund
                now_date = datetime.datetime.now().date()
                # now_date = datetime.datetime(2022, 1, 17).date()
                hold = sum(queryset.filter(expense_type='buy').values_list('hold', flat=True))
                expense = hold * FundValue.objects.get(fund=fund, deal_at=now_date).value
                FundExpense.objects.create(
                    fund=fund, deal_at=now_date, expense=expense, hold=hold, expense_type='sale', sale_at=now_date,
                )
                queryset.update(need_buy_again=True, )

    sale.short_description = "全部出售"

    def hold_value(self, obj):
        if obj.expense_type == 'sale':
            return ""
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
        if obj.expense_type == 'sale':
            return ''
        last_fundvalue = FundValue.objects.filter(fund=obj.fund_value.fund).order_by('deal_at').last()
        value = obj.hold * last_fundvalue.value
        # 卖出去过的，不展示收益率
        if obj.need_buy_again:
            return ''
        else:
            return f"{(((value - obj.expense) / obj.expense) * 100):0.02f}%"

    hold_rate_persent.short_description = '持有收益率'

    def hope_value(self, obj):
        if obj.expense_type == 'sale':
            return ""
        return obj.hope_value

    hope_value.short_description = '期望市值'

    def transaction_rule(self, obj):
        return obj.fund.transaction_rule

    transaction_rule.short_description = '交易规则'

    def can_sale_hold(self, obj):
        """ 获得最佳可售份额 """
        if obj.expense_type == 'sale':
            return ""

        fund = obj.fund
        # 最优出售天数, 一般短线 7 天，长线 30 天。
        best_transaction_rule_days = fund.best_transaction_rule_days

        # 最优出售日期，一般短线为 7 天后免手续费
        best_rule_date = datetime.datetime.now() - datetime.timedelta(days=best_transaction_rule_days + 1)

        # 所有购买记录
        all_buy_hold = sum(list(
            FundExpense.objects.filter(fund=obj.fund, expense_type='buy', ).values_list(
                'hold', flat=True)))
        # 所以出售记录
        all_sale_hold = sum(list(
            FundExpense.objects.filter(fund=obj.fund, expense_type='sale', ).values_list(
                'hold', flat=True)))
        # 当前拥有份额
        hold = all_buy_hold - all_sale_hold

        # 近 7 天或 30 天内的购买记录，这部分要手续费
        resently_buy_hold = sum(list(
            FundExpense.objects.filter(fund=obj.fund, expense_type='buy', deal_at__gt=best_rule_date).values_list(
                'hold', flat=True)))

        can_sale_hold = hold - resently_buy_hold
        fund_value = FundValue.objects.filter(fund=obj.fund, ).order_by('deal_at').last()
        return f"{can_sale_hold:0.02f}/{(fund_value.value * can_sale_hold):0.02f}"

    can_sale_hold.short_description = '可售份额/等价金额'

    def get_changelist_instance(self, request):
        result = super().get_changelist_instance(request=request)
        # 显示购买金额
        instance = result.queryset.first()
        if instance:
            expense = sum(FundExpense.objects.filter(
                fund=instance.fund, expense_type='buy', need_buy_again=False
            ).values_list('expense', flat=True))
            expense = round(expense, 2)
            result.title += f', 购买金额：{expense} 元'
        return result


@admin.register(FundHoldings)
class FundHoldingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'catetory_name', 'expense', 'hold', 'persent')

    def persent(self, obj):
        result = obj.expense * 100 / max(list(FundHoldings.objects.values_list('expense', flat=True)))
        return f"{result:0.02f}%"

    persent.short_description = '仓位占比'
