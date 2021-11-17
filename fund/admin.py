from django import forms
from django.contrib import admin
from django.utils.html import format_html

from fund.models import Fund, FundValue, FundExpense


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rate', 'expense', 'value', 'pyramid',)
    search_fields = ['name', ]
    list_filter = ('name',)

    def expense(self, obj):
        expense = FundExpense.objects.filter(fund=obj).values_list('expense', flat=True)
        return round(sum(expense), 2)

    expense.short_description = '已投入资金'

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
        hold = sum(FundExpense.objects.filter(fund=obj).values_list('hold', flat=True))
        fund_value = FundValue.objects.filter(fund=obj, ).order_by('deal_at').last()
        if not fund_value:
            return '0'
        hope_value = 0
        for fund_expense in FundExpense.objects.filter(fund=obj):
            hope_value += fund_expense.hope_value
        if hold * fund_value.value > hope_value:
            result = f"""<span style="color: red;">{(hold * fund_value.value):0.02f}</span>"""
        else:
            result = f"""<span style="color: green;">{(hold * fund_value.value):0.02f}</span>"""
        return format_html(f"""{result}/{hope_value:0.02f}　　　　　""")

    value.short_description = '金额/止赢金额✌️'

    def pyramid(self, obj):

        fund_value = FundValue.objects.filter(fund=obj, ).order_by('deal_at').last()
        当前净值_index = None
        html_list = []
        for index, stage in enumerate(obj.pyramid_stage):

            if obj.from_value > obj.to_value:
                if fund_value.value > stage and 当前净值_index is None:
                    rate = (stage - fund_value.value) * 100 / fund_value.value
                    html_list.append(f"当前净值: {fund_value.value:.4f}；下阶段 ⬇️ 涨幅:{rate:.2f}%　　　　　</br>")
                    当前净值_index = len(html_list)

            elif obj.from_value < obj.to_value:
                if fund_value.value > stage and 当前净值_index is None:
                    rate = (fund_value.value - stage) * 100 / fund_value.value
                    html_list.append(f"当前净值: {fund_value.value:.4f}；下阶段 ⬆️ 涨幅:{rate:.2f}%　　　　　　　　　　　</br>")
                    当前净值_index = len(html_list)

            html_list.append(
                f"{index:02} 仓位: 市值: {stage:.4f}；总投入: {(1 + index) * index / 2 * obj.space_expense}　　　　　　</br>")

        if obj.from_value < obj.to_value and 当前净值_index is None:
            rate = (stage - fund_value.value) * 100 / fund_value.value
            html_list.append(f"当前净值: {fund_value.value:.4f}；下阶段 ⬆️ 涨幅:{rate:.2f}%　　　　　　　　　　　</br>")
            当前净值_index = len(html_list)

        if 当前净值_index is None:
            当前净值_index = 0
        html_slice_start = 当前净值_index - 3
        html_slice_start = 0 if html_slice_start < 0 else html_slice_start
        html_slice_end = 当前净值_index + 2
        html_list = html_list[html_slice_start:html_slice_end]

        if fund_value:
            html_list.append(f"净值走势：{obj.from_value} --> {fund_value.value} --> {obj.to_value}　　　　　　　　　　</br>")

        return format_html(''.join(html_list))

    pyramid.short_description = '金字塔'


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
        fee = self.cleaned_data['fund'].fee
        hold = FundExpense.get_hold(fund_value=fund_value.value, expense=self.cleaned_data['expense'], fee=fee)
        self.cleaned_data['hold'] = hold
        return self.cleaned_data


@admin.register(FundExpense)
class FundExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'deal_at', 'fund', 'hold', 'expense', 'hold_value', 'hope_value')
    search_fields = ['fund__name', 'id', ]
    list_filter = ('fund__name',)
    actions = ['sum_hold', ]
    form = FundExpenseForm

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

    def hope_value(self, obj):
        return obj.hope_value

    hope_value.short_description = '期望市值'
