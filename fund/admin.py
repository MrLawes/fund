from django.contrib import admin

# Register your models here.
from fund.models import Fund


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code',)
    fields = ('name', 'code',)
