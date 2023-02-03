from django.contrib import admin

from cademy.models import MathCademy


@admin.register(MathCademy)
class MathCademyAdmin(admin.ModelAdmin):
    list_display = ('id',)
