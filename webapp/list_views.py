import datetime

from django.shortcuts import render

from finance import low_pb_pctl as pb, score_boad as sb


def score_boad(request):
    df = sb.screen_stocks()
    html = df.to_html(escape=False)
    context = {'df': html}
    df.to_csv(f'd:/tmp/stocks{datetime.date.today()}.csv')
    return render(request, 'webapp/stocks.html', context)


def low_pb_pctl(request):
    df = pb.screen_stocks()
    html = df.to_html(escape=False)
    context = {'df': html}
    return render(request, 'webapp/stocks.html', context)
