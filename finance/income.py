import datetime
import math

import akshare as ak
import pandas as pd

from finance import utils, const
from finance.utils import cache


def get(code):
    key = 'income' + code
    df = cache.get(key)
    if df is None:
        try:
            df = ak.stock_profit_sheet_by_report_em(symbol=utils.prefix(code))
            df = df[
                ['SECURITY_CODE', 'REPORT_DATE', 'UPDATE_DATE', 'TOTAL_OPERATE_INCOME', 'TOTAL_OPERATE_INCOME_YOY',
                 'OPERATE_INCOME',
                 'OPERATE_INCOME_YOY', 'TOTAL_OPERATE_COST', 'TOTAL_OPERATE_COST_YOY', 'OPERATE_COST',
                 'OPERATE_COST_YOY', 'RESEARCH_EXPENSE', 'SALE_EXPENSE', 'FINANCE_EXPENSE', 'FAIRVALUE_CHANGE_INCOME',
                 'INVEST_INCOME', 'OPERATE_PROFIT', 'OPERATE_PROFIT_YOY', 'TOTAL_PROFIT', 'TOTAL_PROFIT_YOY',
                 'NETPROFIT', 'NETPROFIT_YOY', 'PARENT_NETPROFIT', 'PARENT_NETPROFIT_YOY', 'DEDUCT_PARENT_NETPROFIT',
                 'DEDUCT_PARENT_NETPROFIT_YOY']]
            df.set_index("REPORT_DATE", inplace=True)
            df.index.name = None
            df = df.head(20).fillna(0)
            df = df.iloc[::-1]
            df['OPERATE_INCOME_Q'] = df[
                'OPERATE_INCOME'].diff()
            df['DEDUCT_PARENT_NETPROFIT_Q'] = df[
                'DEDUCT_PARENT_NETPROFIT'].diff()
            for d in df.index:
                # print(d)
                [year, quarter, day] = d.split(' ')[0].split('-')
                df.loc[d, 'year'] = year
                df.loc[d, 'quarter'] = quarter
                if d.find('03-31') > 0:
                    df.loc[d, 'DEDUCT_PARENT_NETPROFIT_Q'] = \
                        df.loc[d, 'DEDUCT_PARENT_NETPROFIT']
                    df.loc[d, 'OPERATE_INCOME_Q'] = \
                        df.loc[d, 'OPERATE_INCOME']
            df = df.iloc[::-1]
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


@cache.memoize(typed=True, expire=const.HALF_DAY)
def enrich(source_df):
    source_df['扣非同比|环比'] = source_df['id'].map(lambda c: do_enrich(get(c)))


@cache.memoize(typed=True, expire=const.HALF_DAY)
def do_enrich(stock_df):
    if stock_df is None:
        return 0, 0
    try:
        stock_df['DEDUCT_PARENT_NETPROFIT_Q'] = stock_df['DEDUCT_PARENT_NETPROFIT_Q'].astype(float)
        quarter_ = stock_df[stock_df['quarter'] == stock_df['quarter'][0]]
        growth_y = quarter_['DEDUCT_PARENT_NETPROFIT_Q'][0] / quarter_['DEDUCT_PARENT_NETPROFIT_Q'][1] - 1
        growth_q = stock_df['DEDUCT_PARENT_NETPROFIT_Q'][0] / stock_df['DEDUCT_PARENT_NETPROFIT_Q'][1] - 1
        return round(math.log10(growth_y * 100), 2) if growth_y > 0 else -0.1, \
               round(math.log10(growth_q * 100), 2) if growth_q > 0 else -0.1
    except Exception as e:
        print("exception in do_enrich of income", e.__cause__, e, stock_df.head())
        return 0, 0


@cache.memoize(typed=True, expire=const.HALF_DAY)
def get_indicator(code, indicator, num=1):
    return get(code)[indicator][:num].sum()


if __name__ == "__main__":
    # start = datetime.datetime.now()
    # s = get("301302")
    # quarter_ = s[s['quarter'] == s['quarter'][0]]
    # # growth = quarter_['DEDUCT_PARENT_NETPROFIT_Q'][0] / quarter_['DEDUCT_PARENT_NETPROFIT_Q'][1] - 1
    # print(s[['DEDUCT_PARENT_NETPROFIT_Q', 'quarter']])
    # end = datetime.datetime.now()
    # print(end - start)
    # # cache.delete("income300327")
    df = ak.stock_profit_sheet_by_report_em(symbol=utils.prefix('300601'))
    # df.to_csv('income.csv')
    print(df['FINANCE_EXPENSE'])
