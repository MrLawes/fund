from django.contrib import admin
from django.utils.html import format_html

from cademy.models import MathCademy


@admin.register(MathCademy)
class MathCademyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_with_host', 'process', 'remark',)
    # 点击进入可编辑部分
    fields = ('name', 'process', 'host', 'remark',)

    def name_with_host(self, obj):
        return format_html(f'<a href="{obj.host}" target="_blank">{obj.name}</a>')

    name_with_host.short_description = "网站名称"
