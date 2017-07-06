import datetime

import django.http
from django.utils import timezone
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure

import rainmaker.models


def historical_loan_rates(request):
    data = rainmaker.models.LendStats.objects.all()
    interest_rate = data.values_list('avg_interest_ask', flat=True)
    over_time = data.values_list('created_at', flat=True)
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.plot_date(over_time, interest_rate, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%b, %d %H:%M'))
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    response = django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response