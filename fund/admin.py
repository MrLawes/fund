import datetime

from django import forms
from django.contrib import admin
from django.utils.html import format_html

from fund.models import Fund, FundValue, FundExpense


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'space_expense', 'expense', 'hope_expense', 'hold_space',)

    def hold_space(self, obj):
        expense = FundExpense.objects.filter(fund=obj).values_list('expense', flat=True)
        expense = sum(expense)
        return round(expense * 10.0 / obj.total_space_expense, 2)

    hold_space.short_description = '持有仓位'

    def expense(self, obj):
        expense = FundExpense.objects.filter(fund=obj).values_list('expense', flat=True)
        return round(sum(expense), 2)

    expense.short_description = '投入资金'

    def hope_expense(self, obj):
        """ 期望投入资金 """
        max_value = max(obj.from_value, obj.to_value)
        min_value = min(obj.from_value, obj.to_value)
        fund_value = FundValue.objects.filter(fund=obj, ).order_by('deal_at').last()
        expense, next_rate = 0, 0

        if not fund_value:
            return expense
        if min_value < fund_value.value < max_value:
            half = min_value + (max_value - min_value) / 2
            duration = (max_value - half) / 10.0
            # 购买的机会
            if obj.from_value > obj.to_value:
                stage = int((half - fund_value.value) / duration)
                for i in range(1, stage + 1):
                    if i != stage:
                        expense += i * obj.space_expense
                    else:
                        next_rate = round(((half - stage * duration) - fund_value.value) / fund_value.value, 4) * 100
                return f"{stage}/{(stage + 1) * obj.space_expense}/{next_rate}/{half - (stage + 1) * duration:0.04f}"
        return expense

    hope_expense.short_description = '本阶段/下阶段投入/下个阶段净值涨跌/下个阶段净值'

@admin.register(FundValue)
class FundValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'fund', 'deal_at', 'value', 'rate',)
    search_fields = ['fund__name', 'deal_at', ]

    def get_queryset(self, request):
        result = super().get_queryset(request=request).order_by('-deal_at', )
        return result


class FundExpenseForm(forms.ModelForm):
    class Meta:
        model = FundExpense
        fields = "__all__"

    def clean(self):
        fund_value = FundValue.objects.get(fund=self.cleaned_data['fund'], deal_at=self.cleaned_data['deal_at'])
        # self.cleaned_data['fund_value'] = fund_value
        hold = FundExpense.get_hold(fund_value=fund_value.value, expense=self.cleaned_data['expense'])
        self.cleaned_data['hold'] = hold
        return self.cleaned_data


@admin.register(FundExpense)
class FundExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'fund_value', 'hold', 'expense', 'hold_value', 'hope_value')
    form = FundExpenseForm


    def hold_value(self, obj):
        last_fundvalue = FundValue.objects.filter(fund=obj.fund_value.fund).order_by('deal_at').last()
        value = round(obj.hold * last_fundvalue.value, 2)
        hope_value = self.hope_value(obj=obj)
        # todo 写入数据库
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
