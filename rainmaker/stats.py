# segmented_rates = range(0, 1001)
# segmented_rates_percent = [utils.BitcoinDecimal(rate)/1000 for rate in segmented_rates]
# segmented_rates_dict = dict((rate_band, 0) for rate_band in segmented_rates_percent)
import time

import decimal

import poloapi.restapi
import rainmaker.models
import rainmaker.utils

def log_loan_rate():
    bid_asks = []
    p = poloapi.restapi.poloniex()
    loans = p.returnLoanOrders('BTC')['offers']
    print len(loans)
    for loan in loans[:25]:
        percent = decimal.Decimal(loan['rate']) * 100
        # floor_percent = floor.quantize(utils.BitcoinDecimal('.001'))
        bid_asks.append(percent)
        # segmented_rates_dict[floor_percent] += utils.BitcoinDecimal(loan['rate'])
    avg_low_bid = sum(bid_asks)/ len(bid_asks)
    return avg_low_bid

def save_lending_stats():
    # time.sleep(10)
    p = poloapi.restapi.poloniex()
    objects_list = []
    loans = p.returnLoanOrders('BTC')['offers']
    for loan in loans:
        percent = decimal.Decimal(loan['rate']) * 100
        amount = rainmaker.utils.BitcoinDecimal(loan['amount'])
        objects_list.append(rainmaker.models.LendHistory(amount=amount,
                                                         rate=percent))
    rainmaker.models.LendHistory.objects.bulk_create(objects_list)
    print objects_list
