from django.contrib import admin

from wikisyntax.models import Blob


class BlobAdmin(admin.ModelAdmin):
    raw_id_fields = ['defer']
    search_fields = ['string']
    list_display = ['string']
    list_filter = ['prefix']

admin.site.register(Blob, BlobAdmin)
