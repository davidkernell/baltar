import django.forms
import django.utils.functional
from django.db import models

import custom_fields


class LendHistory(models.Model):
    amount = custom_fields.BitcoinField()
    interest_ask = models.DecimalField(max_digits=6, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)


class LendStats(models.Model):
    avg_interest_ask = models.DecimalField(max_digits=8, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)
