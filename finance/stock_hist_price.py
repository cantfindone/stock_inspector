import datetime

import akshare as ak
import numpy as np

from finance import utils
from finance.utils import cache


@cache.memoize()
def get_range(code, start_date_str, end_date_str):
    return ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date_str, end_date=end_date_str,
                              adjust="hfq")


@cache.memoize()
def get(code, date_str):
    date = date_str
    if isinstance(date_str, str):
        date = utils.parse_date(date_str)
    date_str = utils.trade_day(date).strftime('%Y%m%d')
    df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=date_str, end_date=date_str,
                            adjust="hfq")
    if len(df) == 0:
        start_date_str = (date - datetime.timedelta(days=1000)).strftime('%Y%m%d')
        df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date_str, end_date=date_str,
                                adjust="hfq")
        print('get price', code, start_date_str, date_str)
    return df[-1:].reset_index()


@cache.memoize()
def price_diff(code, start_date, end_date):
    try:
        p1 = get(code, start_date)['收盘'][0]
        p2 = get(code, end_date)['收盘'][0]
        diff = (p2 - p1) / p1
        return round(diff, 2)
    except Exception as e:
        print("price_diff exception:", code, e.__cause__, e)
        return np.NaN


if __name__ == "__main__":
    # print(utils.latest_n_trade_days_of(utils.parse_date('20200104')))
    # print(utils.last_trade_day(utils.parse_date('20200104')))
    # print(utils.trade_day(utils.parse_date('20021101')))
    # print(utils.trade_day(utils.parse_date('20221101')))
    # print(get('000001', '20021101'))
    # print(get('000001', '20221101'))
    # print(get('601299', '20221101'))
    print(get('000831', '20121101'))
