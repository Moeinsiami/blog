from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin


# admin.sites.AdminSite.site_header = "پنل مدیر جنگو"
# admin.sites.AdminSite.site_title = "پنل مدیر"
# admin.sites.AdminSite.index_title = "پنل"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'status']
    ordering = ['title', 'publish']
    list_filter = ['status', 'author', ('publish', JDateFieldListFilter)]
    search_fields = ['title', 'description']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug': ['title']}
    list_editable = ['status']
    # list_display_links = ['author']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'phone']
