import datetime

from django import forms
from django.contrib import admin
from django.db import transaction
from django.utils import timezone
from django.utils.html import format_html

from fund.models import Fund, FundValue, FundExpense, FundHoldings


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_html', 'rate', 'expense', 'month_min',)
    search_fields = ['name', ]
    list_filter = ('name', 'high_sale_low_buy',)

    def get_queryset(self, request):
        return super().get_queryset(request=request).order_by('-newest_rate')

    def expense(self, obj):
        expense = FundExpense.objects.filter(fund=obj, expense_type='buy').values_list('expense', flat=True, )  # noqa
        remark = '(弃投)' if obj.id in [1, 3, 6, 7, 8, 9, 10, 11, 16, ] else ''
        return f"{sum(expense):,.2f}{remark}"

    expense.short_description = '已投入资金'

    def name_html(self, obj):
        return format_html(f'<a href="/admin/fund/fundexpense/?fund__name={obj.name}" target="_blank">{obj.name}</a>')

    name_html.short_description = '基金名称'

    def rate(self, obj):
        fund_value: FundValue = FundValue.objects.filter(fund=obj).order_by('deal_at').last()  # noqa
        if not fund_value:
            return 0
        rate = fund_value.rate
        if rate > 0:
            rate = f"""<span style="color: red;">{rate}</span>"""
        else:
            rate = f"""<span style="color: green;">{rate}</span>"""
        return format_html(f"({str(fund_value.deal_at)[5:]}) {rate}　　　")

    rate.short_description = '估算涨幅'

    def month_min(self, obj):
        min_value, min_deal_at = 999999, ''
        for fund_value in FundValue.objects.filter(  # noqa
                fund=obj, deal_at__gte=datetime.datetime.now() - datetime.timedelta(days=31)
        ):
            if fund_value.value < min_value:
                min_value = fund_value.value
                min_deal_at = fund_value.deal_at

        now = datetime.datetime.now()
        name_prefix = obj.name.split(']')[0] + "]"
        this_month_buy = FundExpense.objects.filter(  # noqa
            fund__name__startswith=name_prefix,
            deal_at__year=now.year,
            deal_at__month=now.month,
            expense_type='buy'
        ).exists()
        this_month_buy = '本月已购买' if this_month_buy else ''

        last_fund_value = FundValue.objects.filter(fund=obj).order_by('deal_at').last()  # noqa
        now_value = last_fund_value.value if last_fund_value else 0
        rate = f"{((now_value - min_value) / min_value) * 100:.2f}"
        if str(min_deal_at) == str(datetime.datetime.now().date()):
            return format_html(f"""<span style="color: red;">{min_deal_at} (↑{rate}) {this_month_buy}</span>""")
        return f'{min_deal_at} (↑{rate}) {this_month_buy}'

    month_min.short_description = '30天内最低'


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

    def __init__(self, *args, **kwargs):
        super(FundExpenseForm, self).__init__(*args, **kwargs)
        self.fields['fund'].queryset = Fund.objects.order_by('name')  # noqa

    def clean(self):
        fund_value = FundValue.objects.get(fund=self.cleaned_data['fund'], deal_at=self.cleaned_data['deal_at'])  # noqa
        # 买入费率
        fee = self.cleaned_data['fund'].fee
        # 扣除买入费率，计算出购买份额
        total_expense = self.cleaned_data['expense']
        total_hold = FundExpense.get_hold(fund_value=fund_value.value, expense=total_expense, fee=fee)
        split_hold = self.cleaned_data.get('split_hold', 0)
        if split_hold:  # 如果需要拆分
            # 创建一份拆分后的交易记录
            split_expense = round(self.cleaned_data['expense'] * split_hold / total_hold, 2)  # noqa
            self.cleaned_data['split_hold'] = 0
            self.cleaned_data['expense'] = split_expense
            self.cleaned_data['hold'] = split_hold
            FundExpense.objects.create(**self.cleaned_data)  # noqa
            # 修改原交易数据
            self.cleaned_data['expense'] = round(total_expense - split_expense, 2)  # noqa
            self.cleaned_data['hold'] = round(total_hold - split_hold, 2)  # noqa
        else:  # 不拆分，记录下总的份额
            self.cleaned_data['hold'] = total_hold
        return self.cleaned_data


@admin.register(FundExpense)
class FundExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'deal_at', 'fund_name', 'hold', 'expense', 'hold_value', 'hold_rate_persent', 'annual_interest_rate', 'expectation',
        'buttons',
    )
    search_fields = ['fund__name', 'id', ]
    list_filter = ('fund__category', 'fund__high_sale_low_buy', 'fund__is_advance', 'fund__name',)
    actions = ['sum_hold', 'sale', ]
    form = FundExpenseForm
    list_per_page = 500

    def get_queryset(self, request):
        results = super().get_queryset(request=request).order_by('-hold_rate')
        return results

    def fund_name(self, obj):
        result = ''
        if obj.expense_type == 'buy':
            if obj.need_buy_again:
                result = f'<a style="text-decoration: line-through" href="/admin/fund/fundexpense/?fund__name={obj.fund.name}" target="_blank">{obj.fund.name}</a>'
            else:
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
                hold = sum(queryset.filter(expense_type='buy').values_list('hold', flat=True))
                expense = hold * FundValue.objects.get(fund=fund, deal_at=now_date).value  # noqa
                FundExpense.objects.create(  # noqa
                    fund=fund, deal_at=now_date, expense=expense, hold=hold, expense_type='sale', sale_at=now_date,
                )
                queryset.update(need_buy_again=True, )

    sale.short_description = "全部出售"

    def hold_value(self, obj):
        if obj.expense_type == 'sale':
            return ""
        last_fundvalue = FundValue.objects.filter(fund=obj.fund_value.fund).order_by('deal_at').last()  # noqa
        value = round(obj.hold * last_fundvalue.value, 2)  # noqa
        color = 'green'
        return format_html(f'<span style="color: {color};">{value}</span>')

    hold_value.short_description = '持有市值'

    def hold_rate_persent(self, obj):
        last_fundvalue = FundValue.objects.filter(fund=obj.fund_value.fund).order_by('deal_at').last()  # noqa
        value = obj.hold * last_fundvalue.value
        if obj.expense == 0:
            fund_value = obj.fund_value
            return f"{(((last_fundvalue.value - fund_value.value) / fund_value.value) * 100):0.02f}%"

        return f"{(((value - obj.expense) / obj.expense) * 100):0.02f}%"

    hold_rate_persent.short_description = '持有收益率'

    def expectation(self, obj: FundExpense):

        localdate = timezone.localdate()
        days = (localdate - obj.deal_at).days
        expect_expense = obj.expense * ((1 + 0.1 / 365) ** days)
        return f"{expect_expense:0.02f}"

    expectation.short_description = '期望金额年化(10%)'

    def get_changelist_instance(self, request):
        result = super().get_changelist_instance(request=request)
        # 显示购买金额
        instance = result.queryset.first()

        if instance:

            expense, hold, fund_value = 0, 0, 0

            for r in result.queryset:
                if r.expense_type == 'buy':
                    expense += r.expense
                    hold += r.hold
                    fund_value += FundValue.objects.filter(fund=r.fund).order_by("deal_at").last().value * r.hold  # noqa
                elif r.expense_type == 'sale':
                    expense -= r.expense
                    hold -= r.hold
                    fund_value -= FundValue.objects.filter(fund=r.fund).order_by("deal_at").last().value * r.hold  # noqa
            expense = int(expense)
            hold = round(hold, 2)  # noqa
            lose = (expense - int(fund_value)) * 100 / expense
            lose = -round(lose, 2)  # noqa
            if lose < 0:
                lose = f'亏损：{lose}%'
            else:
                lose = f'盈利：{lose}%'

            # 基金类型
            result.title += f'，投入：{expense} 元；持有份额：{hold}；市值：{int(fund_value)}({int(fund_value) - expense}); {lose}'

        return result


@admin.register(FundHoldings)
class FundHoldingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'catetory_name', 'expense', 'hold', 'persent')

    def persent(self, obj):
        result = obj.expense * 100 / max(list(FundHoldings.objects.values_list('expense', flat=True)))  # noqa
        return f"{result:0.02f}%"

    persent.short_description = '仓位占比'
