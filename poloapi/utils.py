import dynamic_settings.models
from poloapi.restapi import poloniex

class TradeCoin:
    def __init__(self, coin):
        if not isinstance(coin, str):
            ValueError('Coin value is not a string')
        coin = dynamic_settings.models.Coin.objects.get(ticker=coin.upper())
        self.coin = coin
        self.coin_ticker = coin.ticker
        trade_settings = dynamic_settings.models.DynamicTradeSetting.objects.get(coin=coin)
        self.can_trade = trade_settings.can_trade
        self.trade_limit = trade_settings.trade_limit
        self.can_buy = trade_settings.can_buy
        self.can_sell = trade_settings.can_sell

    def marginBuy(self, coin_ticker):
        p = poloniex()