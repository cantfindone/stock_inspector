import datetime

import akshare as ak
import numpy as np
from finance import stock_info, a_stocks, stock_hist_price, bond_cov
import pandas

from finance import utils


# print([np.nan for i in range(4)])


def 上市后区间涨幅(code, days=[5, 10, 20]):
    na_rt = tuple([np.nan for i in range(len(days)+1)])
    rt = []
    daily = bond_cov.hist(code)
    if daily is None:
        return na_rt
    daily = daily['收盘价']
    daily = daily.dropna().reset_index()
    daily = daily['收盘价']
    已上市 = np.where(daily != 100)
    if len(已上市[0]) == 0:
        return na_rt
    off_set = 已上市[0][0]
    rt.append(daily[off_set])
    # print(已上市)
    for day_range in days:
        try:
            if day_range + off_set >= len(daily):
                rt.append(np.nan)
            else:
                区间涨幅 = daily[day_range + off_set] / daily[off_set] - 1
                rt.append(round(区间涨幅, 4))
            # print(区间涨幅)
        except Exception as e:
            print("Exception:", e.__cause__, day_range, daily)
    return tuple(rt)


df = bond_cov.get().dropna(subset=['上市时间'])
a = df.apply(lambda c: 上市后区间涨幅(c['债券代码'], [5, 10, 20]), axis=1, result_type='expand')
df[['首日收盘价', '5日涨幅', '10日涨幅', '20日涨幅']] = a
df = df.dropna(subset=['20日涨幅'])
df.to_csv("out/历史可转债上市后区间涨幅.csv")
print("上市5日区间涨幅:", df['5日涨幅'].mean())
print("上市10日区间涨幅:", df['10日涨幅'].mean())
print("上市20日区间涨幅:", df['20日涨幅'].mean())

# print(上市后区间涨幅('118019', [5, 10, 20]))
