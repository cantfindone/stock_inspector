import math

import akshare as ak

from finance import utils, income, const
from finance.utils import load_stock, dump_stock, cache


@cache.memoize(typed=True, expire=const.HALF_DAY)
def get(code):
    table = 'stock_indicator'
    stock_a_lg_indicator_df = load_stock(table, code)
    if stock_a_lg_indicator_df is None:
        stock_a_lg_indicator_df = ak.stock_a_lg_indicator(symbol=code)
        stock_a_lg_indicator_df = stock_a_lg_indicator_df.iloc[::-1]
        stock_a_lg_indicator_df = stock_a_lg_indicator_df.head(2000)
        stock_a_lg_indicator_df['roe'] = stock_a_lg_indicator_df['pb'] / stock_a_lg_indicator_df['pe_ttm']
        dump_stock(stock_a_lg_indicator_df, table, code)
    # print(code, len(stock_a_lg_indicator_df))
    stock_a_lg_indicator_df['roe'] = stock_a_lg_indicator_df['pb'] / stock_a_lg_indicator_df['pe_ttm']
    stock_a_lg_indicator_df.insert(loc=0, column='股票代码', value=code)

    return stock_a_lg_indicator_df.fillna(0)


def enrich(source_df):
    source_df['roe|dv|pe|pepctl|pbpctl'] = source_df['id'].map(lambda c: do_enrich(c))


@cache.memoize(typed=True, expire=const.HALF_DAY)
def do_enrich(c):
    stock_df = get(c)
    try:
        stock_df.reset_index(inplace=True)
        pe_ttm_de = stock_df['total_mv'][0] / income.get_indicator(c, 'DEDUCT_PARENT_NETPROFIT_Q', 4) * 10000
        print('pe_ttm_de of ', c, ":", pe_ttm_de)
        print('pe_ttm of ', c, ":", stock_df['pe_ttm'][0])
        val = round(math.log(stock_df['roe'].mean() * 100 / 18, 2), 2), \
              1 * round(math.log(stock_df['dv_ttm'][:600].mean() + 0.1), 2), \
              -2 if pe_ttm_de <= 0 else round(math.log(1 / pe_ttm_de / 0.05), 2), \
              1 * round(1 - utils.cal_percentile(True, stock_df['pe_ttm']), 2), \
              1 * round(1 - utils.cal_percentile(True, stock_df['pb']), 2)
        return val

    except Exception as e:
        print('do_enrich exception in stock_indicator', e.__cause__, e, '\n',
              stock_df.head()[['股票代码', 'roe', 'dv_ttm', 'pe_ttm', 'pb']])
    return 0, 0, 0, 0, 0


if __name__ == "__main__":
    df = get('000159')
    print(df.columns)
