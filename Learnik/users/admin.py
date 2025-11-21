from django.contrib import admin

from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')
    readonly_fields = ('password_hash',)
