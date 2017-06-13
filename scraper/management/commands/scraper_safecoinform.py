import json

import logging
import requests
import twilio.rest

import dynamic_settings.models
import scraper.models

from django.conf import settings


def check_for_safe_dev_post():
    FORM_URL = 'http://forum.safedev.org/'
    DEV_ACCT_ID = 205

    known_posts = scraper.models.MaidSafeFormPost.objects.values_list('topic_id', flat=True)
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
                        logging.warning('attempting margin buy on safecoin for the amount of {} btc'.format(settings.SAFECOIN_DEVPOST_TRADE))

                    else:
                        logging.warning('MaidSafeCoin dynamic trading turned off')
                        continue

    logging.info('SafeCoin form scraped, no new dev posts')
