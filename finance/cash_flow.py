import datetime

import akshare as ak
import pandas as pd

from finance import utils, const
from finance.utils import cache


# @cache.memoize(typed=True, expire=const.HALF_DAY)
def get(code):
    key = 'cash_flow' + code
    df = cache.get(key)
    if df is None:
        try:
            df = ak.stock_cash_flow_sheet_by_yearly_em(symbol=utils.prefix(code))
            df = df[
                ['SECURITY_CODE', 'REPORT_DATE', 'NETCASH_FINANCE', 'NETCASH_FINANCE_YOY',
                 'NETCASH_INVEST',
                 'NETCASH_INVEST_YOY', 'NETCASH_OPERATE', 'NETCASH_OPERATE_YOY', 'NETPROFIT', 'NETPROFIT_YOY']]
            df.set_index("REPORT_DATE", inplace=True)
            df.index.name = None
            df = df.fillna(0)
            days = (pd.to_datetime(df.index)[0] + datetime.timedelta(days=365) - datetime.datetime.now()).days
            days = max(days, 5)
            cache.set(key, df, expire=const.ONE_DAY * days, tag=code)
        except Exception as e:
            print("get cash_flow_df exception:", e.__cause__, e, code)
    return df


@cache.memoize(typed=True, expire=const.HALF_DAY)
def is_good(code):
    df = get(code)
    if df is None:
        return False
    # if 'CONTRACT_LIAB' not in df.columns.tolist():
    #     return True
    try:
        df = df.iloc[:5, ::]
        # return df['NETCASH_OPERATE'].sum() > df['NETCASH_INVEST'].sum()
        return df['NETCASH_FINANCE'].mean() < df['NETCASH_OPERATE'].mean() * 0.1 and df['NETCASH_OPERATE'].mean() > 0
    except Exception as e:
        print("is good except in cash_flow", e, code, df)
        return False


@cache.memoize(typed=True, expire=const.HALF_DAY)
def enrich(source_df):
    source_df['现金流'] = source_df['id'].map(lambda c: 1 if is_good(c) else 0)


if __name__ == "__main__":
    # start = datetime.datetime.now()
    # print(get("601117"))
    # end = datetime.datetime.now()
    # print(end - start)
    # df = ak.stock_cash_flow_sheet_by_yearly_em(symbol=utils.prefix('601117'))
    df = ak.stock_cash_flow_sheet_by_quarterly_em(symbol=utils.prefix('601117'))
    print(df['SALES_SERVICES'])