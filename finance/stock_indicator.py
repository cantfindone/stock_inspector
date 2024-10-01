import datetime
import math

import akshare as ak

from finance import utils, income, const
from finance.utils import cache


@cache.memoize(typed=True, expire=const.ONE_DAY * 1)
def get(code):
    # key = 'stock_indicator' + code
    # df = cache.get(key)
    # if df is None or len(df) == 0:
    df = ak.stock_a_indicator_lg(symbol=code)
    df = df.iloc[::-1]
    df = df.head(1800)
    df['roe'] = df['pb'] / df['pe_ttm']
    df['roe'] = df['pb'] / df['pe_ttm']
    df.insert(loc=0, column='股票代码', value=code)
    df = df.reset_index()
    # print(df.head(1))
    df = df.fillna(0)
    # days = 90 if len(df) == 0 else (
    #         pd.to_datetime(df['trade_date'])[0] + datetime.timedelta(days=90) - datetime.datetime.now()).days
    # days = max(days, 1)
    # days = 1
    # cache.set(key, df, expire=const.ONE_DAY * days, tag=code)
    return df


def enrich(source_df):
    source_df['roe|dv|pe|pepctl|pbpctl'] = source_df['id'].map(lambda c: do_enrich(c))


# @cache.memoize(typed=True, expire=const.HALF_DAY)
def do_enrich(c):
    try:
        stock_df = get(c).head(1500)
        stock_df.reset_index(inplace=True)
        pe_ttm_de = stock_df['total_mv'][0] / income.get_indicator(c, 'DEDUCT_PARENT_NETPROFIT_Q', 4) * 10000
        # print('pe_ttm_de of ', c, ":", pe_ttm_de)
        # print('pe_ttm of ', c, ":", stock_df['pe_ttm'][0])
        val = round(math.log(stock_df['roe'].mean() * 100 / 18, 2), 2), \
              2 * round(math.log(stock_df['dv_ttm'][0] + 0.1, 5), 2), \
              -2 if pe_ttm_de <= 0 else round(math.log(1 / pe_ttm_de / 0.05) * 3, 2), \
              1 * round(1 - utils.cal_percentile(True, stock_df['pe_ttm']), 2), \
              1 * round(1 - utils.cal_percentile(True, stock_df['pb']), 2)
        # 2 * round(math.log(stock_df['dv_ttm'][:600].mean() + 0.1, 5), 2), \
        return val


    except Exception as e:
        print('do_enrich exception in stock_indicator', c, e.__cause__, e, '\n')
        # stock_df.head()[['股票代码', 'roe', 'dv_ttm', 'pe_ttm', 'pb']])
    return 0, 0, 0, 0, 0


if __name__ == "__main__":
    print(get("603619"))
    start = datetime.datetime.now()
    print(do_enrich("603619"))
    end = datetime.datetime.now()
    print(end - start)

    # print(ak.stock_a_lg_indicator(symbol='301367'))
    print(income.get_indicator("603619", 'DEDUCT_PARENT_NETPROFIT_Q', 4))
