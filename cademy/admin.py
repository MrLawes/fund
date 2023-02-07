from django.contrib import admin
from django.utils.html import format_html

from cademy.models import MathCademy, TechnologyCademy


class BaseCademyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'host_with_link', 'process', 'remark',)
    # 点击进入可编辑部分
    fields = ('name', 'process', 'host', 'remark',)

    def host_with_link(self, obj):
        return format_html(f'<a href="{obj.host}" target="_blank">{obj.host}</a>')

    host_with_link.short_description = "网站地址"


@admin.register(MathCademy)
class MathCademyAdmin(BaseCademyAdmin):
    pass


@admin.register(TechnologyCademy)
class TechnologyCademyAdmin(BaseCademyAdmin):
    pass
