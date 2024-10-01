import akshare as ak
from finance.utils import cache
from finance import const


@cache.memoize(typed=True, expire=const.ONE_DAY * 0.5)
def get_all():
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    spot = stock_zh_a_spot_em_df[
        ['代码', '名称', '最新价', '市盈率-动态', '市净率', '总市值', '60日涨跌幅', '年初至今涨跌幅']]
    spot.set_index('代码', inplace=True)
    return spot


def get(code):
    return cache.get('spot' + code)


def cache_all():
    get_all().apply(lambda row: cache.set('spot' + row.name, row, expire=const.ONE_DAY * 0.5), axis=1)


if __name__ == "__main__":
    # cache_all()
    df = get('688500')
    print(df)
