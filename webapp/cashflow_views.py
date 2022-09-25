from django.shortcuts import render
from pandas.core.dtypes.common import is_numeric_dtype

from finance import cash_flow
from finance.utils import plot_columns


def get(request, code, name):
    df = cash_flow.get(code)
    df.index = df.index.map(lambda x: x.split(' ')[0])
    df = df.iloc[:5, :]
    df.loc['mean'] = df.apply(lambda s: s.mean() if is_numeric_dtype(s) else s[-1])
    df.insert(loc=1, column="名称", value=name)
    html = df.to_html(escape=False)
    context = {'df': html}
    return render(request, 'webapp/factors.html', context)


def plot(request, code, name):
    df = cash_flow.get(code)
    df.index = df.index.map(lambda x: x.split(' ')[0])
    df = df.iloc[::-1]
    df = df.iloc[:, 1:]
    print(df.head())
    images = plot_columns(df, title=name)
    context = {'images': images}
    return render(request, 'webapp/plots.html', context)
