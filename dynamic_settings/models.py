from __future__ import unicode_literals

from django.db import models

from custom_fields import BitcoinField


class Coin(models.Model):
    ticker = models.CharField(max_length=5)
    name = models.CharField(max_length=16)
    on_poloniex = models.BooleanField(default=False)
    on_coinbase = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     self.ticker = self.ticker.upper()
    #     super(Coin, self).save(self, *args, **kwargs)


class DynamicTradeSetting(models.Model):
    coin = models.ForeignKey(Coin)
    can_trade = models.BooleanField(default=False)
    trade_limit = BitcoinField(default=0)
    can_buy = models.BooleanField(default=False)
    can_sell = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
