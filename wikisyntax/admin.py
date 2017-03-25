from django.contrib import admin

from wikisyntax.models import Blob


class BlobAdmin(admin.ModelAdmin):
    list_display = ['string']
    list_filter = ['prefix']

admin.site.register(Blob, BlobAdmin)
