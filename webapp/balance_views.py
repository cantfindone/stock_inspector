from django.shortcuts import render

from finance import balance_sheet
from finance.utils import plot_columns


def get(request, code, name):
    df = balance_sheet.get(code)
    df.set_index("REPORT_DATE", inplace=True)
    df.index.name = None
    df.index = df.index.map(lambda x: x.split(' ')[0])
    df.insert(loc=2, column="名称", value=name)
    html = df.to_html(escape=False)
    context = {'df': html}
    return render(request, 'webapp/factors.html', context)


def plot(request, code, name):
    df = balance_sheet.get(code)
    df.set_index("REPORT_DATE", inplace=True)
    df.index.name = None
    df.index = df.index.map(lambda x: x.split(' ')[0])
    df = df.iloc[::-1]
    df = df.iloc[:, 2:]
    print(df.head())
    images = plot_columns(df, title=name)
    context = {'images': images}
    return render(request, 'webapp/plots.html', context)
