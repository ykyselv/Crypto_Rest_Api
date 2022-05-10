from django.contrib import admin
from .models import Crypto


@admin.register(Crypto)
class CryptoAdmin(admin.ModelAdmin):
    list_display = ['time_create','cp_curr','curr','price', 'course_stability']
    list_per_page = 10
    list_editable = ['price']

    @admin.display(ordering='price')
    def course_stability(self, crypto:Crypto):
        if crypto.price < 2000:
            return 'low stability'
        elif crypto.price < 12000 and crypto.price > 2000:
            return 'average stability'
        elif crypto.price > 12000:
            return 'high stability'

