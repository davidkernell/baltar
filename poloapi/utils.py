import decimal

import time

class BitcoinDecimal(decimal.Decimal):
    def __init__(self, *args, **kwargs):
        super(BitcoinDecimal, self).__init__(*args, **kwargs)
        self.decimal_places = 8
        self.max_digits = 16
        self.default = 0

    # def __name__(self):
    #     return 'BitcoinDecimal'

def save_lending_stats():
    time.sleep(10)
