import datetime

import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype

from finance import finance_indicator, stock_indicator, balance_sheet, cash_flow_quarter, performance, income, a_stocks, \
    stock_zygc_ym, const, spot_em, valuation
from finance.utils import sum_tuple, cache


# @cache.memoize(typed=True, expire=const.ONE_HOUR/6)
def screen_stocks():
    print(datetime.datetime.now(), 'get_gt_3y()')
    print(datetime.datetime.now(), 'spot_em.cache_all()', spot_em.cache_all())
    all_df = a_stocks.get_gt_3y()[['代码', '市盈率-动态', '60日涨跌幅', '年初至今涨跌幅']]
    print(datetime.datetime.now(), 'performance.get()')
    df = performance.get()
    df = df.rename(columns={'股票代码': 'id'})
    print(datetime.datetime.now(), 'merge')
    df = pd.merge(df, all_df, how='inner', left_on='id', right_on='代码')
    df = df[
        (df['id'] < '800000')
        # & (df['营业收入-同比增长'] > 0)
        # & (df['净利润-同比增长'] > 10)
        & (df['销售毛利率'] > 15)
        & (df['所处行业'].str.startswith('房地') == False)
        # & (df['净资产收益率'] > 9)
        # & (df['每股经营现金流量'] > 0)
        & (df['id'].str.startswith('4') == False)
        & (df['id'].str.startswith('2') == False)
        & (df['id'].str.startswith('68') == False)
        ]

    del df['序号']
    del df['每股收益']
    del df['营业收入-营业收入']
    del df['净利润-净利润']
    del df['每股净资产']
    del df['净资产收益率']
    del df['每股经营现金流量']
    # del df['最新公告日期']
    print(datetime.datetime.now(), "finance_indicator.enrich()")
    finance_indicator.enrich(df)
    df = df[df['存货|应收|天数|净利率'].apply(sum_tuple) > 3]
    print(datetime.datetime.now(), 'cash_flow_quarter.enrich()')
    cash_flow_quarter.enrich(df)
    print(datetime.datetime.now(), 'balance_sheet.enrich()')
    balance_sheet.enrich(df)
    # df = df[df['负债|商誉|固定'].apply(lambda x: x[0] > 0)]
    print(datetime.datetime.now(), 'income.enrich()')
    income.enrich(df)
    df = df[df['扣非同比|环比'].apply(lambda x: x[0]) > 0]
    # df = df[df['扣非同比|环比'].apply(sum_tuple) > 0]
    # print(datetime.datetime.now(), 'stock_indicator.enrich()')
    # stock_indicator.enrich(df)
    # df = df[df['roe|dv|pe|pepctl|pbpctl'].apply(lambda x: x[2] > -1.4 and x[0] > -0.5 and x[3] + x[4] > 1.1)]
    print(datetime.datetime.now(), 'valuation.enrich()')
    valuation.enrich(df)
    df = df[df['roe|pe|price_pctl'].apply(lambda x: x[0] > 1 and (x[1] > 1 or x[2] > 2.5))]

    df['score'] = df['存货|应收|天数|净利率'].apply(sum_tuple) \
                  + df['融资|营收现金率'].apply(sum_tuple) \
                  + df['负债|商誉|固定'].apply(sum_tuple) \
                  + df['扣非同比|环比'].apply(sum_tuple) \
                  + df['roe|pe|price_pctl'].apply(sum_tuple)
    # + df['roe|dv|pe|pepctl|pbpctl'].apply(sum_tuple)
    df.sort_values(['score'], inplace=True, ascending=False)
    # df = df.head(100)
    df = df.reset_index()
    del df['index']
    del df['代码']
    df.loc['mean'] = df.apply(lambda s: round(s.mean(), 0) if is_numeric_dtype(s) else 'mean', axis=0)
    df['主业'] = df['id'].map(lambda s: stock_zygc_ym.zyyw(s))
    return df


if __name__ == "__main__":
    t = (1, 2, 3)
    print(sum_tuple(t))
