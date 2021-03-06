import datetime
import decimal
import logging
import time
import twilio.rest
import django.core.management
from django.utils import timezone

import rainmaker.models
from poloapi.restapi import poloniex
from django.conf import settings

class Command(django.core.management.BaseCommand):
    def handle(self, *args, **options):
        try:
            loop_start_time = timezone.now()
            freqency = 30  # seconds
            while 1 > 0:
                if loop_start_time + datetime.timedelta(days=1) < timezone.now():
                    # client = twilio.rest.Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

                    # message = client.messages.create(settings.ADMIN_PHONE,
                    #                                  from_=settings.TWILIO_PHONE,
                    #                                  body=u"BTC Lending stats ended sucessfully")
                    # print(message.sid)
                    break
                p = poloniex()
                bid_asks = []
                loans = p.returnLoanOrders('BTC')['offers']
                i = 0
                for loan in loans:
                    i += 1
                    percent = decimal.Decimal(loan['rate']) * 100
                    if i > 25:
                        bid_asks.append(percent)
                avg_low_bid = sum(bid_asks) / len(bid_asks)
                rainmaker.models.LendStats.objects.create(avg_interest_ask=avg_low_bid)
                logging.info('Save completed at price: {}'.format(avg_low_bid))
                print 'Save completed at price: {}'.format(avg_low_bid)
                loop_start_time = timezone.now()
                time.sleep(freqency)
        except Exception as e:
            client = twilio.rest.Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

            message = client.messages.create(settings.ADMIN_PHONE,
                                             from_=settings.TWILIO_PHONE,
                                             body=u"BTC Lending scrape ended becasue of error - {}".format(e))
            print(message)
