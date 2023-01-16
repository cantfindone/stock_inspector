import akshare as ak
from finance import const
from finance.utils import cache


@cache.memoize(expire=const.ONE_DAY * 10)
def get():
    bond_zh_cov_df = ak.bond_zh_cov()
    # print(bond_zh_cov_df)
    return bond_zh_cov_df[["债券代码", "债券简称", "上市时间", ]]


def hist(code):
    key = 'bond_zh_cov_value_analysis' + code
    df = cache.get(key)
    if df is not None:
        return df
    try:
        df = ak.bond_zh_cov_value_analysis(symbol=code)
        if len(df) > 100:
            cache.set(key, df, expire=const.ONE_DAY * 100, tag='bond_zh_cov_value_analysis')
        # print(df)
    except Exception as e:
        print("exception in bond_zh_cov_value_analysis", code)
        return None
    return df


if __name__ == "__main__":
    print(get())
    d = hist('123167').dropna(subset=['收盘价'])
    print(d)
