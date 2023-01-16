import datetime

from django.shortcuts import render

from finance import industry, utils
from finance.factors import enrich_bank_data


def industries(request):
    df = industry.list_all()

    html = df.to_html(escape=False)
    context = {'df': html}
    return render(request, 'webapp/industry.html', context)


def plot(request, code, name):
    now = datetime.date.today()
    start_date_str = (now - datetime.timedelta(days=1000)).strftime('%Y%m%d')
    end_date_str = now.strftime('%Y%m%d')
    df = industry.hist(name, start_date_str, end_date_str)[['日期', '收盘', '成交额', '换手率']]
    df.reset_index(inplace=True)
    df.set_index('日期', inplace=True)
    del df['index']
    # print(df.head())
    images = utils.plot_columns(df, title=name)
    context = {'images': images}
    return render(request, 'webapp/plots.html', context)


def members(request, code, name):
    df = industry.members(name)
    df.columns = ['id', '名称', '市盈率-动态', '市净率']
    df = enrich_bank_data(df)
    html = df.to_html(escape=False)
    context = {'df': html}
    return render(request, 'webapp/stocks.html', context)
