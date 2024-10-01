import datetime

import akshare as ak
import pandas as pd

from finance import utils, const, stock_info, income_quarter
from finance.utils import cache


def get(code):
    key = 'cash_flow_quarter' + code
    df = cache.get(key)
    if df is None:
        try:
            df = ak.stock_cash_flow_sheet_by_quarterly_em(symbol=utils.prefix(code))
            if 'SALES_SERVICES' in df.columns:
                df = df[
                    ['SECURITY_CODE', 'REPORT_DATE', 'NETCASH_FINANCE', 'NETCASH_INVEST', 'NETCASH_OPERATE',
                     'SALES_SERVICES']]
            else:
                df = df[
                    ['SECURITY_CODE', 'REPORT_DATE', 'NETCASH_FINANCE', 'NETCASH_INVEST', 'NETCASH_OPERATE']]
                df['SALES_SERVICES'] = df['NETCASH_OPERATE'] * 0
            df.set_index("REPORT_DATE", inplace=True)
            df.index.name = None
            df = df.fillna(0)
            now = datetime.datetime.now()
            report_date = pd.to_datetime(df.index)[0]
            days = (report_date + datetime.timedelta(days=(120 if report_date.month != 9 else 180)) - now).days
            days = max(days, 5)
            cache.set(key, df, expire=const.ONE_DAY * days, tag=report_date.strftime('%Y%m%d'))
            print(key, 'expire at ', datetime.datetime.fromtimestamp(cache.get(key, expire_time=True)[1]),
                  'tag=', report_date.strftime('%Y%m%d'))
        except Exception as e:
            print("get cash_flow_quarter exception:", e.__cause__, e, code)
    return df


# @cache.memoize(typed=True, expire=const.HALF_DAY)
def cash_revenue(code):
    cash = get(code).head(12)[['SALES_SERVICES']]
    income = income_quarter.get(code).head(12)[['OPERATE_INCOME']]
    # print(f'cash.index:{cash.index}, income.index:{income.index}')
    cash_income = pd.merge(cash, income, left_index=True, right_index=True)
    # print(cash_income)
    cash_income['cash_revenue'] = cash_income['SALES_SERVICES'] / cash_income['OPERATE_INCOME']
    return cash_income


@cache.memoize(typed=True, expire=const.HALF_DAY)
def do_enrich(code):
    df = get(code)
    na_rt = 0, 0
    if df is None or len(df) == 0:
        return na_rt
    try:
        # df = df.iloc[:5, ::]
        # return df['NETCASH_OPERATE'].sum() > df['NETCASH_INVEST'].sum()
        # list_date = stock_info.list_date(code)
        # years = (datetime.datetime.now() - list_date).days / 365
        operate = df['NETCASH_OPERATE'].mean()
        finance_score = -1 if operate <= 0 else (operate - df['NETCASH_FINANCE'].mean()) / operate
        finance_score = max(finance_score, -1)
        finance_score = min(finance_score, 2)
        revenue_score = df['SALES_SERVICES'][0] / income_quarter.get_indicator(code, 'OPERATE_INCOME', 1)
        return round(finance_score, 1), min(round(revenue_score, 1), 1.5)

    except Exception as e:
        print("do_enrich exception in cash_flow_quarterly", e.__cause__, e, code, '\n', df.head(4).T)
    return na_rt


def enrich(source_df):
    source_df['融资|营收现金率'] = source_df['id'].map(lambda c: do_enrich(c))


if __name__ == "__main__":
    # start = datetime.datetime.now()
    # print(get("601377"))
    # end = datetime.datetime.now()
    # print(end - start)
    # df = ak.stock_cash_flow_sheet_by_yearly_em(symbol=utils.prefix('601117'))
    # df = ak.stock_cash_flow_sheet_by_quarterly_em(symbol=utils.prefix('601117'))
    # print(df['SALES_SERVICES'])
    # print(income_quarter.get('601117'))
    print(cash_revenue('601377'))
