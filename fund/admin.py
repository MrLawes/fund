import datetime

from django import forms
from django.contrib import admin

from fund.models import Fund, FundValue, FundExpense


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'three_yearly_change',)


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
        return round(obj.hold * last_fundvalue.value, 2)

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


""":arg

/Users/chenhaiou/Desktop/D/git/api/venv/bin/python /Users/chenhaiou/Desktop/D/git/cdl_api/api/settings/chenhaiou.py
时间         投入金额/持有市值/恒定市值/期望市值           持有收益/期望收益              期望收益率                持有仓位                 基金名称
----------  --------------------------------------  --------------------------  ----------------------  ----------------------  -----------------------------------------
2021-11-15  500.41/0/0.00/529.49                    -500.41/29.08               5.81%                   0.715                   工银瑞信文体产业股票A[打算出售 146.76 份]
2021-11-15  1000.23/959.63/0.00/1120.43             -40.60/120.20               12.02%                  1.429                   诺安成长混合[打算出售 1 份]
2021-11-15  1139.32/1100.84/0.00/1273.17            -38.48/133.85               11.75%                  1.628                   诺安成长混合[打算出售 2 份]
2021-11-15  1619.00/1629.46/0.00/1788.99            10.46/169.99                10.50%                  2.313                   诺安成长混合[打算出售 3 份]
2021-11-15  2101.49/2155.29/0.00/2300.44            53.80/198.95                9.47%                   3.002                   诺安成长混合[打算出售 4 份]
2021-11-15  2621.98/2732.29/0.00/2844.93            110.31/222.95               8.50%                   3.746                   诺安成长混合[打算出售 5 份]
"""
