from django.conf.urls import url, include

import rainmaker.views

urlpatterns = [
    url('^plot/$', rainmaker.views.historical_loan_rates, name='index')
]