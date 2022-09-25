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
    print(code, len(stock_a_lg_indicator_df))
    stock_a_lg_indicator_df['roe'] = stock_a_lg_indicator_df['pb'] / stock_a_lg_indicator_df['pe_ttm']
    stock_a_lg_indicator_df.insert(loc=0, column='股票代码', value=code)

    return stock_a_lg_indicator_df.fillna(0)


def enrich(source_df):
    source_df['roe|dv|pe|pepctl|pbpctl'] = source_df['id'].map(lambda c: do_enrich(get(c)))


def do_enrich(stock_df):
    return min(round((stock_df['roe'][0] - 0.1) / 0.1, 2), 1), \
           min(round(stock_df['dv_ttm'][:600].mean() * 0.1, 2), 1), \
           1 if stock_df['pe_ttm'][0] < 28 else 0, \
           1 if utils.cal_percentile(True, stock_df['pe_ttm']) < 0.5 else 0, \
           1 if utils.cal_percentile(True, stock_df['pb']) < 0.5 else 0

    if __name__ == "__main__":
        df = get('000159')
    print(df.columns)
