import datetime

import akshare as ak
import pandas as pd

from finance import utils, const
from finance.utils import cache


def get(code):
    key = 'income_quarter' + code
    df = cache.get(key)
    if df is None:
        try:
            df = ak.stock_profit_sheet_by_quarterly_em(symbol=utils.prefix(code))
            df = df[
                ['SECURITY_CODE', 'REPORT_DATE', 'UPDATE_DATE', 'TOTAL_OPERATE_INCOME', 'TOTAL_OPERATE_INCOME_QOQ',
                 'OPERATE_INCOME',
                 'OPERATE_INCOME_QOQ', 'TOTAL_OPERATE_COST', 'TOTAL_OPERATE_COST_QOQ', 'OPERATE_COST',
                 'OPERATE_COST_QOQ', 'RESEARCH_EXPENSE',
                 'RESEARCH_EXPENSE_QOQ', 'SALE_EXPENSE', 'SALE_EXPENSE_QOQ', 'FAIRVALUE_CHANGE_INCOME', 'INVEST_INCOME',
                 'OPERATE_PROFIT', 'OPERATE_PROFIT_QOQ'
                    , 'TOTAL_PROFIT', 'TOTAL_PROFIT_QOQ', 'NETPROFIT', 'NETPROFIT_QOQ'
                    , 'PARENT_NETPROFIT', 'PARENT_NETPROFIT_QOQ', 'DEDUCT_PARENT_NETPROFIT',
                 'DEDUCT_PARENT_NETPROFIT_QOQ']]
            df = df.head(20)
            df.set_index("REPORT_DATE", inplace=True)
            df.index.name = None
            # del df['index']
            for d in df.index:
                # print(d)
                [year, quarter, day] = d.split(' ')[0].split('-')
                df.loc[d, 'year'] = year
                df.loc[d, 'quarter'] = quarter
            now = datetime.datetime.now()
            days = (pd.to_datetime(df.index)[0] + datetime.timedelta(days=(90 if now.month < 12 else 180)) - now).days
            days = max(days, 5)
            # print("days to cache:", days)
            cache.set(key, df, expire=const.ONE_DAY * days, tag=code)
        except Exception as e:
            print("except occurred in get income", e.__cause__, e)
            print("income_df:", df)
    # print(df.head(2))
    # df.head(2).T.to_csv("d:\\income.csv")
    return df


@cache.memoize(typed=True, expire=const.HALF_DAY)
def get_indicator(code, indicator):
    get(code)[indicator][0]


def enrich(source_df):
    source_df['扣非同比|环比'] = source_df['id'].map(lambda c: do_enrich(get(c)))


@cache.memoize(typed=True, expire=const.HALF_DAY)
def do_enrich(stock_df):
    if stock_df is None:
        return 0, 0
    try:
        stock_df['DEDUCT_PARENT_NETPROFIT'] = stock_df['DEDUCT_PARENT_NETPROFIT'].astype(float)
        return 2 if stock_df[stock_df['quarter'] == stock_df['quarter'][0]]['DEDUCT_PARENT_NETPROFIT'][
                    :2].is_monotonic_decreasing else 0, 1 if stock_df['DEDUCT_PARENT_NETPROFIT_QOQ'][0] > 0 else 0
    except Exception as e:
        print("exception in do_enrich of income", e.__cause__, e, stock_df.head())
        return 0, 0


@cache.memoize(typed=True, expire=const.HALF_DAY)
def get_indicator(code, indicator, num=1):
    return get(code)[indicator][:num].sum()


if __name__ == "__main__":
    # start = datetime.datetime.now()
    # print(get("300327"))
    # end = datetime.datetime.now()
    # print(end - start)
    # cache.delete("income_quarter300327")
    df = get('601997')
    # print(df[['TOTAL_OPERATE_INCOME','DEDUCT_PARENT_NETPROFIT','DEDUCT_PARENT_NETPROFIT_QOQ']])
    print(df.head(2).T)
    # df = ak.stock_profit_sheet_by_quarterly_em(symbol=utils.prefix('300327'))
    # print(df.columns.tolist())
