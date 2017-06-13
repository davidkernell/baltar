import django.contrib.admin
import dynamic_settings.models
class CoinAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('ticker', 'name', 'on_poloniex', 'on_coinbase', 'deleted')
    list_filter = ('ticker', 'name', 'on_poloniex', 'on_coinbase', 'deleted')

class DynamicTradeSettingAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('coin', 'can_trade', 'trade_limit', 'can_buy', 'can_sell', 'deleted')
    list_filter = ('coin', 'can_trade', 'trade_limit', 'can_buy', 'can_sell', 'deleted')

django.contrib.admin.site.register(dynamic_settings.models.Coin, CoinAdmin)
django.contrib.admin.site.register(dynamic_settings.models.DynamicTradeSetting, DynamicTradeSettingAdmin)