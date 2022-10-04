import math

import akshare as ak

from finance import utils
from finance.utils import load_stock, dump_stock


def get(code):
    table = 'stock_indicator'
    stock_a_lg_indicator_df = load_stock(table, code)
    if stock_a_lg_indicator_df is None:
        stock_a_lg_indicator_df = ak.stock_a_lg_indicator(symbol=code).head(2000)
        stock_a_lg_indicator_df['roe'] = stock_a_lg_indicator_df['pb'] / stock_a_lg_indicator_df['pe_ttm']
        dump_stock(stock_a_lg_indicator_df, table, code)
    # print(code, len(stock_a_lg_indicator_df))
    stock_a_lg_indicator_df['roe'] = stock_a_lg_indicator_df['pb'] / stock_a_lg_indicator_df['pe_ttm']
    stock_a_lg_indicator_df.insert(loc=0, column='股票代码', value=code)

    return stock_a_lg_indicator_df.fillna(0)


def enrich(source_df):
    source_df['roe|dv|pe|pepctl|pbpctl'] = source_df['id'].map(lambda c: do_enrich(get(c)))


def do_enrich(stock_df):
    try:
        val = min(round(math.log(stock_df['roe'].mean() * 10, 2), 2), 2), \
              2 * min(round(stock_df['dv_ttm'][:600].mean() * 0.2, 2), 1), \
              0 if stock_df['pe_ttm'][0] <= 0 else round(math.log(20 / stock_df['pe_ttm'][0]), 2), \
              2 * round(1 - utils.cal_percentile(True, stock_df['pe_ttm']), 2), \
              2 * round(1 - utils.cal_percentile(True, stock_df['pb']), 2)
        return val
    except Exception as e:
        print('do_enrich exception in stock_indicator', e, )
        return 0, 0, 0, 0, 0


if __name__ == "__main__":
    df = get('000159')
    print(df.columns)
