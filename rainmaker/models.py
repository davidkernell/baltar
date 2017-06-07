from django.db import models

# Create your models here.

class BitcoinField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        super(BitcoinField, self).__init__(*args, **kwargs)
        self.decimal_places = 8
        self.max_digits = 16
        self.default = 0


class LendHistory(models.Model):
    amount = BitcoinField()
    interest_ask = models.DecimalField(max_digits=6, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)


class LendStats(models.Model):
    avg_interest_ask = models.DecimalField(max_digits=8, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)