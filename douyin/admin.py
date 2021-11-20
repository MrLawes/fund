from django.contrib import admin
from django.utils.html import format_html

from douyin.models import DouYinUser


@admin.register(DouYinUser)
class DouYinUserAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'douyin_username', 'first_name_with_head_url', 'create_at', 'relationship', 'fens_count', 'follow_count',)
    search_fields = ['first_name', ]
    exclude = ['id', 'password', 'last_login', 'is_superuser', 'last_name', 'email', 'is_staff', 'is_active',
               'date_joined', 'user_ptr_id', ]

    def douyin_username(self, obj):
        return format_html(f'<a href="{obj.href}&close=false" target="_blank">{obj.username}</a>')

    douyin_username.short_description = '抖音号'

    def first_name_with_head_url(self, obj):
        return format_html(f'<img src="{obj.head_url}" width="30px" height="30px"/> {obj.first_name}')

    first_name_with_head_url.short_description = '抖音名'
