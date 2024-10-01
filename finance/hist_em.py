import akshare as ak
from finance.utils import cache
from finance import const, utils
import datetime


@cache.memoize(typed=True, expire=const.ONE_DAY * 7)
def get(code):
    yesterday = utils.yesterday()
    five_years = yesterday - datetime.timedelta(days=365 * 5 + 1)
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, period="weekly", start_date=five_years.strftime('%Y%m%d'),
                                            end_date=yesterday.strftime('%Y%m%d'),
                                            adjust="hfq")
    stock_zh_a_hist_df = stock_zh_a_hist_df[['日期', '收盘']]
    return stock_zh_a_hist_df.iloc[::-1]


# print(get("000001"))
