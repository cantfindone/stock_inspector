from django.shortcuts import render

from finance import stock_zygc_ym
from finance.utils import plot_columns


def get(request, code, name):
    df = stock_zygc_ym.get(code)
    df.insert(loc=1, column="名称", value=name)
    html = df.to_html(escape=False)
    context = {'df': html}
    return render(request, 'webapp/factors.html', context)


def plot(request, code, name):
    df = stock_zygc_ym.get(code)
    df.set_index("REPORT_DATE", inplace=True)
    df.index.name = None
    df.index = df.index.map(lambda x: x.split(' ')[0].replace('-', ''))
    df = df.iloc[::-1]
    df = df.iloc[:, 4:]
    # print(df.head())
    images = plot_columns(df, title=name)
    context = {'images': images}
    return render(request, 'webapp/plots.html', context)

