import akshare as ak
import numpy as np
from finance import const

from finance.utils import cache


def get(code):
    key = 'stock_zygc_ym' + code
    df = cache.get(key)
    if df is not None:
        print("found stock_zygc_ym in cache")
        return df
    df = ak.stock_zygc_ym(symbol=code)
    if df is not None and len(df) > 0:
        df = df[df['报告期'] == df['报告期'][0]]
        df = df[df['分类'] != '合计']
        df.sort_values(['分类方向', '营业收入-占主营收入比'], ascending=[True, False], inplace=True)
    cache.set(key, df, expire=const.ONE_DAY * 0.5, tag=code)
    return df


@cache.memoize(typed=True, expire=const.ONE_DAY)
def zyyw(code):
    df = get(code)
    df_ = df[df['分类方向'] == '按行业分']
    df = df[df['分类方向'] == '按产品分'] if len(df_) == 0 else df_
    max_ = df[df['营业收入-占主营收入比'] == df['营业收入-占主营收入比'].max()]
    max_ = max_.reset_index()
    max_ = max_['分类']
    print('max_:', max_)
    return max_[0] if len(max_) > 0 else np.NAN


if __name__ == "__main__":
    get('600177')
    get('600177')
    print(get('600177'))
