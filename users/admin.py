"""Настройки админки."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import MyUser

admin.site.empty_value_display = 'Не задано'


class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_editable = (
        'email',
        'first_name',
        'last_name',
    )
    search_fields = ('username', 'email',)
    list_filter = ('username',)
    list_display_links = ('username',)


admin.site.register(MyUser, UserAdmin)
