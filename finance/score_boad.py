import os
from functools import lru_cache
from pathlib import Path

import akshare as ak
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype

from finance import utils, finance_indicator, stock_indicator, balance_sheet, cash_flow, performance, income, a_stocks


def sum_tuple(tuple_like):
    return sum(tuple_like)


@lru_cache
def screen_stocks():
    all_df = a_stocks.get()[['代码', '市盈率-动态', '60日涨跌幅', '年初至今涨跌幅']]

    performance_df = performance.get()
    performance_df = performance_df[
        (performance_df['股票代码'] < '800000')
        & (performance_df['营业收入-同比增长'] > 0)
        & (performance_df['净利润-同比增长'] > 5)
        & (performance_df['净资产收益率'] > 9)
        & (performance_df['每股经营现金流量'] > 0)
        & (performance_df['股票代码'].str.startswith('4') == False)
        & (performance_df['股票代码'].str.startswith('68') == False)
        ]

    del performance_df['序号']
    del performance_df['每股收益']
    del performance_df['营业收入-营业收入']
    del performance_df['净利润-净利润']
    del performance_df['每股净资产']
    del performance_df['每股经营现金流量']
    del performance_df['最新公告日期']
    df = performance_df.rename(columns={'股票代码': 'id'})
    finance_indicator.enrich(df)
    df = df[df['存货|应收'].apply(sum_tuple) > 1]
    cash_flow.enrich(df)
    balance_sheet.enrich(df)
    income.enrich(df)
    df = df[df['扣非同比|环比'].apply(sum_tuple) > 1]
    stock_indicator.enrich(df)
    # df = df[df['roe|dv|pe|pepctl|pbpctl'].apply(sum_tuple) > 2]

    df['score'] = df['存货|应收'].apply(sum_tuple) \
                  + df['cash_flow'] \
                  + df['负债|应收'].apply(sum_tuple) \
                  + df['扣非同比|环比'].apply(sum_tuple) \
                  + df['roe|dv|pe|pepctl|pbpctl'].apply(sum_tuple)
    df.sort_values(['score'], inplace=True, ascending=False)
    df = df.head(50)
    df = df.reset_index()
    del df['index']
    merge = pd.merge(df, all_df, how='inner', left_on='id', right_on='代码')
    merge.loc['mean'] = merge.apply(lambda s: s.mean() if is_numeric_dtype(s) else 'mean', axis=0)

    return merge


if __name__ == "__main__":
    t = (1, 2, 3)
    print(sum_tuple(t))
