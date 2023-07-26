from crypto_app.models import CryptoData
from django.contrib import admin


class CryptoDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'market_cap', 'volume_24h', 'circulating_supply')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('id')


admin.site.register(CryptoData, CryptoDataAdmin)
