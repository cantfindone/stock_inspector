from django.shortcuts import render

from finance import performance, score_boad


def perf(request):
    # df = performance.screen_stocks()
    df = score_boad.screen_stocks()
    html = df.to_html(escape=False)
    context = {'df': html}
    return render(request, 'webapp/stocks.html', context)
