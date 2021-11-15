import datetime

from django import forms
from django.contrib import admin
from django.utils.html import format_html

from fund.models import Fund, FundValue, FundExpense


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'space_expense', 'expense', 'pyramid',)
    search_fields = ['name', ]
    list_filter = ('name',)

    def expense(self, obj):
        expense = FundExpense.objects.filter(fund=obj).values_list('expense', flat=True)
        return round(sum(expense), 2)

    expense.short_description = '已投入资金'

    def pyramid(self, obj):

        fund_value = FundValue.objects.filter(fund=obj, ).order_by('deal_at').last()
        html = ''
        for index, stage in enumerate(obj.pyramid_stage):
            if obj.from_value > obj.to_value:
                if fund_value.value > stage and not '当前市值' in html:
                    rate = (stage - fund_value.value) * 100 / fund_value.value
                    html += f"当前市值: {fund_value.value:.4f}；下阶段 ⬇️ 涨幅:{rate:.2f}%　　　　　</br>"
            elif obj.from_value < obj.to_value:
                if fund_value.value > stage and not '当前市值' in html:
                    rate = (fund_value.value - stage) * 100 / fund_value.value
                    html += f"当前市值: {fund_value.value:.4f}；下阶段 ⬆️ 涨幅:{rate:.2f}%　　　　　</br>"
            html += f"{index:02} 仓位: 市值: {stage:.4f}；总投入: {(1 + index) * index / 2 * obj.space_expense}　　　　　　</br>"

        if obj.from_value < obj.to_value and not '当前市值' in html:
            rate = (stage - fund_value.value) * 100 / fund_value.value
            html += f"当前市值: {fund_value.value:.4f}；下阶段 ⬆️ 涨幅:{rate:.2f}%　　　　　</br>"

        html += f"净值走势：{obj.from_value} --> {fund_value.value} --> {obj.to_value}　　　　　　　　　　</br>"
        return format_html(html)

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
    search_fields = ['fund__name', ]
    list_filter = ('fund__name',)
    form = FundExpenseForm

    def hold_value(self, obj):
        last_fundvalue = FundValue.objects.filter(fund=obj.fund_value.fund).order_by('deal_at').last()
        value = round(obj.hold * last_fundvalue.value, 2)
        hope_value = self.hope_value(obj=obj)
        if hope_value > value:
            color = 'green'
        else:
            color = 'red'

        return format_html(f'<span style="color: {color};">{value}</span>')

    hold_value.short_description = '持有市值'

    def hope_value(self, obj):
        # 天化
        day_change = obj.fund_value.fund.day_change
        # 持有时间
        days = datetime.datetime.now().date() - obj.fund_value.deal_at
        days = days.days
        # 通过天化得期望市值，再加上手续费
        value = ((1 + day_change) ** days) * obj.expense
        value *= 1.0065
        return round(value, 2)

    hope_value.short_description = '期望市值'
