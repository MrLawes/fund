import datetime

from django import forms
from django.contrib import admin
from django.utils.html import format_html

from fund.models import Fund, FundValue, FundExpense


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'three_yearly_change', 'hold_space',)

    def hold_space(self, obj):
        expense = FundExpense.objects.filter(fund_value__fund=obj).values_list('expense', flat=True)
        expense = sum(expense)
        return round(expense * 10.0 / obj.total_space_expense, 2)

    hold_space.short_description = '持有仓位'


@admin.register(FundValue)
class FundValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'fund', 'deal_at', 'value', 'rate',)

    def get_queryset(self, request):
        result = super().get_queryset(request=request).order_by('-deal_at', )
        return result


class FundExpenseForm(forms.ModelForm):
    class Meta:
        model = FundExpense
        fields = "__all__"

    def clean(self):
        hold = FundExpense.get_hold(
            fund_value=self.cleaned_data['fund_value'].value, expense=self.cleaned_data['expense']
        )
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

        if hope_value > value:
            color = 'red'
        else:
            color = 'green'

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

