from django.contrib import admin
from . import models as md


class ListingAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)


admin.site.register(md.Listing, ListingAdmin)
admin.site.register(md.Category)
admin.site.register(md.Bid)
admin.site.register(md.Comment)
