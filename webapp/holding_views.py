import pandas as pd
from django.shortcuts import render

from finance.factors import enrich_data
from webapp.models import Stock


def lists(request):
    stocks = Stock.objects.all().values()
    df = pd.DataFrame(stocks)
    df = df[['id', 'name']]
    df = enrich_data(df)
    html = df.to_html(escape=False)
    context = {'df': html}
    return render(request, 'webapp/stocks.html', context)



