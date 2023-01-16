from django.shortcuts import render

from finance import cash_flow_quarter
from finance.utils import plot_columns


def plot(request, code, name):
    df = cash_flow_quarter.cash_revenue(code)
    df.index = df.index.map(lambda x: x.split(' ')[0].replace('-', ''))
    df = df.iloc[::-1]
    # print(df.head())
    images = plot_columns(df, title=name)
    context = {'images': images}
    return render(request, 'webapp/plots.html', context)
