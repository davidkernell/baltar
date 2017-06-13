import json

import logging

import datetime
import django.core.management
import ratelimit
from django.utils import timezone
import requests
import twilio.rest
import time
import dynamic_settings.models
import scraper.models

from django.conf import settings


class Command(django.core.management.BaseCommand):

    def handle(self, *args, **options):
        task_start_time = timezone.now()
        loop_start_time = None
        freqency = 30  # seconds
        seconds_in_hour = 60 * 60
        num_loops = (seconds_in_hour / freqency)
        FORM_URL = 'http://forum.safedev.org/'
        DEV_ACCT_ID = 205
        dev_post = False

        known_posts = scraper.models.MaidSafeFormPost.objects.values_list('topic_id', flat=True)
        for x in xrange(num_loops):
            if loop_start_time:
                time_since_last = timezone.now() - loop_start_time
                if loop_start_time and time_since_last < datetime.timedelta(seconds=freqency):
                    while time_since_last < datetime.timedelta(seconds=freqency):
                        logging.warning('Save fired too quickly since last save. Time since last save {}'.format(
                            time_since_last.seconds))
                        print 'Save fired too quickly since last save. Time since last save {}'.format(
                            time_since_last.seconds)
                        time.sleep(.5)
                        time_since_last = timezone.now() - loop_start_time
            loop_start_time = timezone.now()
            page = requests.get(FORM_URL)
            # dirty as hell
            start_str = 'ps.store("topic_list_latest"'
            end_str = '}]}]}});\n'
            data_start = page.content.find(start_str) + len(start_str) + 2
            data_end = page.content.find(end_str, data_start) + len(end_str) - 3
            post_data = json.loads(page.content[data_start:data_end])
            for topic in post_data['topic_list']['topics']:
                if topic['id'] in known_posts:
                    continue
                for posters in topic['posters']:
                    if posters[u'description'] == u'Original Poster':
                        scraper.models.MaidSafeFormPost.objects.create(topic_id=topic['id'],
                                                                       dev_blog=True if posters[
                                                                                            'user_id'] == DEV_ACCT_ID else False)
                        if posters['user_id'] == DEV_ACCT_ID:
                            client = twilio.rest.Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

                            message = client.messages.create(settings.ADMIN_PHONE,
                                                             from_=settings.TWILIO_PHONE,
                                                             body="NEW MAIDSAFE DEV POST!\n{}".format(FORM_URL))
                            print(message.sid)
                            logging.warning('New Dev Post Found!')
                            dev_post = True
                            try:
                                coin = dynamic_settings.models.Coin.objects.get(ticker='MAID')
                            except:
                                logging.warning('MaidSafeCoin not found in Coin DB')
                            try:
                                coin_settings = dynamic_settings.models.DynamicTradeSetting.objects.get(coin=coin)
                            except:
                                logging.warning('MaidSafeCoin dynamic settings found in Coin DB')
                                continue
                            if coin_settings.can_trade:
                                logging.warning('attempting margin buy on safecoin for the amount of {} btc'.format(
                                    settings.SAFECOIN_DEVPOST_TRADE))

                            else:
                                logging.warning('MaidSafeCoin dynamic trading turned off')
                                continue
            if not dev_post:
                logging.info('SafeCoin form scraped, no new dev posts')
            time_since_start = timezone.now() - task_start_time
            print time_since_start
            time.sleep(freqency)
        if time_since_start > datetime.timedelta(hours=1):
            logging.info('Hourly Task started at {} and ended at {} UTC'.format(task_start_time.isoformat(), timezone.now()))
            return