from django.contrib import admin

# Register your models here.
from fund.models import Fund, FundValue


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'three_yearly_change',)
    fields = ('name', 'code', 'three_yearly_change',)


@admin.register(FundValue)
class FundValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'fund', 'deal_at', 'value', 'rate',)
    fields = ('fund', 'deal_at', 'value', 'rate',)
