from django.contrib import admin

from polls.models import StaticToken


class StaticTokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    fields = ('user',)
    ordering = ('-created',)


admin.site.register(StaticToken, StaticTokenAdmin)
