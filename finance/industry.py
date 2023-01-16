import datetime

import akshare as ak
from pandas.core.dtypes.common import is_numeric_dtype

from finance import const, stock_info, stock_hist_price, utils
from finance.utils import cache


@cache.memoize(expire=const.ONE_DAY * 10)
def list_all():
    df = ak.stock_board_industry_name_em()

    df = df[['板块代码', '板块名称', '总市值']]
    now = datetime.date.today()
    start_date_str = (now - datetime.timedelta(days=1000)).strftime('%Y%m%d')
    end_date_str = now.strftime('%Y%m%d')
    df['百分位'] = df['板块名称'].map(lambda i: percentile(i, start_date_str, end_date_str))
    df = df.sort_values(['百分位'], ascending=True)
    df.reset_index(inplace=True)
    del df['index']
    return df


@cache.memoize(expire=const.ONE_DAY * 1)
def hist(name, start_date_str, end_date_str):
    df = ak.stock_board_industry_hist_em(symbol=name, start_date=start_date_str, end_date=end_date_str, period="月k",
                                         adjust="hfq")
    return df


@cache.memoize(expire=const.ONE_DAY * 1)
def percentile(name, start_date_str, end_date_str):
    hist_s = hist(name, start_date_str, end_date_str)['收盘']
    return utils.cal_percentile(False, hist_s)


def members(name):
    df = ak.stock_board_industry_cons_em(symbol=name)
    return df[['代码', '名称', '市盈率-动态', '市净率']]


if __name__ == "__main__":
    # print(members('小金属'))
    print(hist('小金属', '20200101', '20221201'))
    # print(hist('小金属','20200101','20221201')['收盘'])
