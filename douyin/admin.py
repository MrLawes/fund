from django.contrib import admin

from douyin.models import DouYinUser


@admin.register(DouYinUser)
class DouYinUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'fens_count')
    search_fields = ['name', ]
