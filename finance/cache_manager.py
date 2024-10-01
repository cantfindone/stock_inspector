import datetime

import akshare as ak
import pandas as pd

from finance import utils, const
from finance.utils import cache


def delete(code, latest_report_date: str):
    prefixes = ['finance_indicator', 'balance_sheet', 'income_quarter', 'income', 'cash_flow_quarter', 'cash_flow']
    for prefix in prefixes:
        key = prefix + code
        df, tag = cache.get(key, tag=True)
        if df is not None and (tag is None or len(tag) == 6 or tag < latest_report_date):
            cache.delete(key)


def expire_stale():
    dates = utils.report_dates(1)
    print(dates)
    report_date = dates[-1].strftime('%Y%m%d')
    df = ak.stock_yjbb_em(date=report_date)
    df['股票代码'].map(lambda c: delete(c, report_date))


if __name__ == "__main__":
    delete('300796', '20230331')
    df, ts, tag = cache.get('income_quarter300482', expire_time=True, tag=True)
    print(datetime.datetime.fromtimestamp(ts), tag)
    print("len(tag):", len(tag))
