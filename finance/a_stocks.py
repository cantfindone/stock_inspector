import akshare as ak
from pandas.core.dtypes.common import is_numeric_dtype

from finance import const, stock_info, stock_hist_price
from finance.utils import cache


@cache.memoize(expire=const.ONE_DAY * 1)
def get():
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    print('stock_zh_a_spot_em:\n',stock_zh_a_spot_em_df)
    stock_zh_a_spot_em_df = stock_zh_a_spot_em_df[stock_zh_a_spot_em_df['代码'] < '800000']
    return stock_zh_a_spot_em_df[['代码', '名称', '市盈率-动态', '60日涨跌幅', '年初至今涨跌幅']]
    # print(stock_zh_a_spot_em_df)


@cache.memoize(expire=const.ONE_DAY * 1)
def get_gt_3y():
    df = get()
    df.dropna(subset='60日涨跌幅', inplace=True)
    df['gt3y'] = df['代码'].map(lambda x: stock_info.listed_gt_3y(x))
    df = df[df['gt3y']]
    return df


@cache.memoize(expire=const.ONE_DAY * 1)
def get_gt_20y():
    df = get()
    df['gt20y'] = df['代码'].map(lambda x: stock_info.listed_gt_20y(x))
    df['上市时间'] = df['代码'].map(lambda x: stock_info.list_date(x))
    df = df[df['gt20y']]
    del df['gt20y']
    return df


@cache.memoize(expire=const.ONE_DAY * 10)
def get_gt_10y():
    df = get()
    df['gt10y'] = df['代码'].map(lambda x: stock_info.listed_gt_10y(x))
    df['上市时间'] = df['代码'].map(lambda x: stock_info.list_date(x))
    df = df[df['gt10y']]
    del df['gt10y']
    return df


if __name__ == "__main__":
    # print(get().info)
    # df = get_gt_20y()
    # print(df.shape)
    # df = df[df['名称'].str.match('中国')]
    # df['20年上涨倍数'] = df['代码'].map(lambda x: stock_hist_price.price_diff(x, '20021101', '20221101'))
    # df.loc['mean'] = df.apply(lambda s: round(s.mean(), 0) if is_numeric_dtype(s) else '-', axis=0)
    # print(df)
    # print(df.shape)
    # df = get_gt_10y()
    # # df['上市时间'] = df['代码'].map(lambda x: stock_info.list_date(x))
    # df = df[df['名称'].str.match('中国')]
    # print(df.shape)
    # df['10年涨幅'] = df['代码'].map(lambda x: stock_hist_price.price_diff(x, '20121101', '20221101'))
    # df.sort_values(['10年涨幅'],inplace=True)
    # df.loc['mean'] = df.apply(lambda s: round(s.mean(), 2) if is_numeric_dtype(s) else '-', axis=0)
    # df.dropna(inplace=True)
    # df.reset_index(inplace=True)
    # del df['index']
    # print(df)
    # df.to_csv("d:\\data.csv")
    df = get()
    # df= df[df['代码']=='601133']
    df.dropna(subset='60日涨跌幅', inplace=True)
    print(df.head())
