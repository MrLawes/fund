from django.contrib import admin

from douyin.models import DouYinUser


@admin.register(DouYinUser)
class DouYinUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'douyin_username', 'first_name', 'create_at', 'relationship', 'fens_count', 'follow_count',)
    search_fields = ['name', ]
    exclude = ['id', 'password', 'last_login', 'is_superuser', 'last_name', 'email', 'is_staff', 'is_active',
               'date_joined', 'user_ptr_id', ]

    def douyin_username(self, obj):
        return obj.username

    douyin_username.short_description = '抖音号'
