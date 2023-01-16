import akshare as ak
from pandas.core.dtypes.common import is_numeric_dtype

from finance import const, stock_info, stock_hist_price
from finance.utils import cache


@cache.memoize(expire=const.ONE_DAY * 10)
def get(code):
    df = ak.index_stock_hist(symbol=code)
    # print(df)
    return df


if __name__ == "__main__":
    df = get("sh000300")
    df = df[(df['in_date'] < '2012-11-01') & (df['out_date'] > '2012-11-01')]
    df.reset_index(inplace=True)
    del df['index']
    print(df)
    print(df.drop_duplicates().shape)

