import django.utils.functional
from django.db import models


class BitcoinField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        super(BitcoinField, self).__init__(*args, **kwargs)
        self.decimal_places = 8
        self.max_digits = 16
        self.default = 0


class RoundingDecimalField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        super(models.DecimalField, self).__init__(*args, **kwargs)
        self.decimal_places = 6
        self.max_digits = 10
        self.default = 0

    @django.utils.functional.cached_property
    def validators(self):
        return super(models.DecimalField, self).valdators

    def formfield(self, **kwargs):
        defaults = {
            'max_digits': self.max_digits,
            'decimal_places': 6,
            'form_class': django.forms.DecimalField,
        }
        defaults.update(kwargs)
        return super(RoundingDecimalField, self).formfield(**defaults)
