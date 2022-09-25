from django.shortcuts import render

from finance import stock_indicator, finance_indicator
from finance.utils import plot_columns


def indicator(request, code, name):
    df = stock_indicator.get(code)
    df.insert(loc=2, column="名称", value=name)
    html = df.to_html(escape=False)
    context = {'df': html, 'factors': df.columns.tolist()[3:], 'code': code, 'name': name}
    return render(request, 'webapp/factors.html', context)


def plot(request, code, name):
    df = stock_indicator.get(code)
    df.set_index("trade_date", inplace=True)
    df = df.iloc[::-1]
    df = df.iloc[:, 1:]
    print(df.head())
    images = plot_columns(df, title=name)
    context = {'images': images}
    return render(request, 'webapp/plots.html', context)


def plot_finance(request, code, name):
    df = finance_indicator.get(code)
    df.set_index("日期", inplace=True)
    df = df.iloc[::-1]
    print(df.head()['存货周转天数(天)'])
    # df = df.iloc[:, 1:]
    images = plot_columns(df, title=name)
    context = {'images': images}
    return render(request, 'webapp/plots.html', context)
