import pandas as pd
from django.shortcuts import render

from finance import finance_indicator, cash_flow, balance_sheet, stock_indicator, income
from webapp.models import Stock
from finance.utils import sum_tuple

def lists(request):
    stocks = Stock.objects.all().values()
    df = pd.DataFrame(stocks)
    df = df[['id', 'name']]
    df = enrich_data(df)
    html = df.to_html(escape=False)
    context = {'df': html}
    return render(request, 'webapp/stocks.html', context)


def enrich_data(df):
    # print(df)
    finance_indicator.enrich(df)
    cash_flow.enrich(df)
    balance_sheet.enrich(df)
    stock_indicator.enrich(df)
    income.enrich(df)

    # df['score'] = df['finance_indicator'] + df['cash_flow'] + df['balance_sheet'] + df['roe']
    # df['score'] = 1 if df['存货|应收'][0] else 0 + 1 if df['存货|应收'][1] else 0 #+ df['cash_flow'] + df['合同负债'] + df['roe']
    df['score'] = df['存货|应收'].apply(sum_tuple) \
                  + df['cash_flow'] \
                  + df['负债|应收'].apply(sum_tuple) \
                  + df['扣非同比|环比'].apply(sum_tuple) \
                  + df['roe|dv|pe|pepctl|pbpctl'].apply(sum_tuple)
    df.sort_values(['score'], inplace=True, ascending=False)
    df.reset_index(inplace=True)
    del df['index']
    return df
