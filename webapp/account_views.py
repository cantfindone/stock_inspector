import matplotlib
from akshare import stock_account_statistics_em
from django.shortcuts import render

from finance.utils import plot_columns

# matplotlib.rc("font", family='Microsoft YaHei')


def plot(request):
    df = stock_account_statistics_em()
    df.set_index("数据日期", inplace=True)
    df = df.iloc[::-1]
    # print(df.head())
    images = plot_columns(df)
    context = {'images': images}
    return render(request, 'webapp/plots.html', context)


