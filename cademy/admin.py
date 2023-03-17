from django.contrib import admin
from django.utils.html import format_html

from cademy.models import Cademy


@admin.register(Cademy)
class CademyAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'host_with_link', 'process', 'remark',)
    # 点击进入可编辑部分
    fields = ('name', 'category', 'every_day', 'process', 'host', 'remark',)
    search_fields = ['name', 'remark', ]
    list_filter = ('category', 'process', 'every_day',)

    def host_with_link(self, obj):
        return format_html(f'<a href="{obj.host}" target="_blank">{obj.host}</a>')

    host_with_link.short_description = "网站地址"
