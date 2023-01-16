import datetime

import akshare as ak
import numpy as np
from finance import stock_info, a_stocks, stock_hist_price
import pandas

from finance import utils


# print([np.nan for i in range(4)])


def 开板后区间涨幅(code, days=[10, 20, 30]):
    na_rt = tuple([np.nan for i in range(len(days) + 2)])
    rt = []
    start_date = stock_info.list_date(code)
    end_date = (start_date + datetime.timedelta(days=90)).strftime('%Y%m%d')
    start_date = start_date.strftime('%Y%m%d')
    rt.append(start_date)
    daily = stock_hist_price.get_range(code, start_date, end_date)
    if len(daily) == 0:
        return na_rt
    daily = daily[['日期', '收盘', '涨跌幅', '振幅', '换手率']]
    daily['涨停'] = daily.apply(lambda d: d['涨跌幅'] > 43 or (d['振幅'] == 0 and d['涨跌幅'] > 9.8), axis=1)
    # print(daily)
    where = np.where(daily['涨停'] == False)
    # print(where)
    if len(where[0]) == 0:
        print("where:", where)
        return na_rt
    开板日 = where[0][0]
    rt.append(开板日)
    # if 开板日 == 0:
    #     print("开板日早于统计日：", code, daily)
    #     return na_rt
    for day_range in days:
        # print("day_range:", day_range)
        截止日 = where[0][0] + day_range
        if 截止日 >= len(daily)+1:
            # rt.append(np.nan)
            return na_rt
        # print(开板日)
        # print(截止日)
        区间涨幅 = daily['收盘'][截止日] / daily['收盘'][开板日] - 1
        rt.append(round(区间涨幅, 4))
        # print(区间涨幅)
    return tuple(rt)


df = a_stocks.get()[['代码', '名称']]
# df = df.head(5)
a = df.apply(lambda c: 开板后区间涨幅(c['代码'], [5, 10, 20]), axis=1, result_type='expand')
print(a)
df[['上市日期', '板数', '5日涨幅', '10日涨幅', '20日涨幅']] = a
df = df.dropna()
print(df)
# print(b)
# print(c)
# print(d)
# print('len(a)',len(a))
# print('len(b)',len(b))
# print('len(c)',len(c))
# print('len(d)',len(d))
# print('len(df)',len(df))
# df[['板数', '5日涨幅', '10日涨幅', '20日涨幅']] = zip(*df['代码'].map(lambda c: 开板后区间涨幅(c, [5, 10, 20])))
# df[['板数', '5日涨幅', '10日涨幅', '20日涨幅']]=a,b,c,d
# df['板数']=a
# df[['板数', '5日涨幅', '10日涨幅', '20日涨幅']] = zip(df.map(lambda c: 开板后区间涨幅(c, [5, 10, 20])))
# print(df)
# print(df['代码'].head(2).map(lambda c: 开板后区间涨幅(c, [5, 10, 20])))
# df['开板5日区间涨幅'] = df['代码'].map(lambda c: 开板后区间涨幅(c, 5))
# df['开板10日区间涨幅'] = df['代码'].map(lambda c: 开板后区间涨幅(c, 10))
# df['开板20日区间涨幅'] = df['代码'].map(lambda c: 开板后区间涨幅(c, 20))
df.dropna(inplace=True)
print(df)
#
df.to_csv("out/历史次新股开板后区间涨幅.csv")
print("开板5日区间涨幅:", df['5日涨幅'].mean())
print("开板10日区间涨幅:", df['10日涨幅'].mean())
print("开板20日区间涨幅:", df['20日涨幅'].mean())
