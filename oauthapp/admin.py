from django.contrib import admin

# Register your models here.
from oauthapp.models import ClientsCodes, Client


class OauthClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'name', 'date_add')
    list_display_links = ('id', 'name')
    list_per_page = 50


class OauthClientCodesAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_add')
    list_display_links = ('id',)
    list_per_page = 50


admin.site.register(Client, OauthClientAdmin)
admin.site.register(ClientsCodes, OauthClientCodesAdmin)
