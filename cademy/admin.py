from django.contrib import admin

from cademy.models import MathCademy


@admin.register(MathCademy)
class MathCademyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'process', 'host')
    # 点击进入可编辑部分
    fields = ('name', 'process', 'host')
