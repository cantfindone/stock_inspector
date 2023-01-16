import datetime

import akshare as ak

from finance.utils import cache
from finance import const


@cache.memoize()
def get(code):
    df = ak.stock_individual_info_em(symbol=code).reset_index().set_index(["item"])
    del df['index']
    return df


@cache.memoize()
def list_date(code):
    try:
        list_day = str(get(code).loc['上市时间']['value'])
        if list_day.strip() == '-':
            return datetime.datetime.now() + datetime.timedelta(days=30)
        return datetime.datetime.strptime(list_day, "%Y%m%d")
    except Exception as e:
        print("list_date exception", e.__cause__, e, code)
        raise Exception(e)


@cache.memoize(expire=const.ONE_DAY * 100)
def name(code):
    try:
        return get(code).loc['股票简称']['value']
    except Exception as e:
        print("list_date exception", e.__cause__, e, code)
        raise Exception(e)


def listed_gt_3y(code):
    key = "listed_gt_3y" + code
    rt = cache.get(key)
    if rt is not None:
        return rt
    gt_3y = (datetime.datetime.now() - list_date(code)).days > 3 * 365
    if gt_3y:
        cache.set(key, gt_3y)
    else:
        cache.set(key, gt_3y, expire=const.ONE_DAY * 10)
    return gt_3y


def listed_gt_20y(code):
    key = "listed_gt_20y" + code
    rt = cache.get(key)
    if rt is not None:
        return rt
    gt_20y = (datetime.datetime.now() - list_date(code)).days > 20 * 366
    if gt_20y:
        cache.set(key, gt_20y)
    else:
        cache.set(key, gt_20y, expire=const.ONE_DAY * 10)
    return gt_20y


def listed_gt_10y(code):
    key = "listed_gt_10y" + code
    rt = cache.get(key)
    if rt is not None:
        return rt
    gt_10y = (datetime.datetime.now() - list_date(code)).days > 10 * 366
    if gt_10y:
        cache.set(key, gt_10y)
    else:
        cache.set(key, gt_10y, expire=const.ONE_DAY * 10)
    return gt_10y


if __name__ == "__main__":
    start = datetime.datetime.now()
    print(get("688432"))
    print(name("688432"))
    end = datetime.datetime.now()
    print(end - start)
    print(list_date("688432"))
    print(listed_gt_3y("688432"))

    print(cache.volume())
