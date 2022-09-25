from django.shortcuts import render

from finance import income
from finance.utils import plot_columns


def get(request, code, name):
    df = income.get(code)
    # df.index = df.index.map(lambda x: x.split(' ')[0])
    df = df[['SECURITY_CODE','DEDUCT_PARENT_NETPROFIT','DEDUCT_PARENT_NETPROFIT_Q', 'year', 'quarter']]
    df.insert(loc=1, column="名称", value=name)

    html = df.to_html(escape=False)
    context = {'df': html}
    return render(request, 'webapp/factors.html', context)


def plot(request, code, name):
    df = income.get(code)
    df = df[['SECURITY_CODE','DEDUCT_PARENT_NETPROFIT','DEDUCT_PARENT_NETPROFIT_Q']]
    df.index = df.index.map(lambda x: x.split(' ')[0])
    df = df.iloc[::-1]
    df = df.iloc[:, 1:]
    print(df.head())
    images = plot_columns(df, title=name)
    context = {'images': images}
    return render(request, 'webapp/plots.html', context)
