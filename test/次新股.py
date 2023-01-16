import datetime

import akshare as ak
import numpy as np
import pandas

from finance import utils

print([np.nan for i in range(4)])


def 开板后区间涨幅(code, days=[10, 20]):
    na_rt = tuple([np.nan for i in range(len(days) + 1)])
    rt = []
    today = utils.today()
    end_date = utils.trade_day(today).strftime('%Y%m%d')
    start_date = (today - datetime.timedelta(days=90)).strftime('%Y%m%d')
    daily = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="hfq")
    if len(daily) == 0:
        return na_rt
    daily = daily[['日期', '收盘', '涨跌幅', '振幅', '换手率']]
    daily['涨停'] = daily.apply(lambda d: d['振幅'] == 0 and d['涨跌幅'] > 9.8, axis=1)
    # print(daily)
    where = np.where(daily['涨停'] == False)
    # print(where)
    if len(where[0]) == 0:
        print("where:", where)
        return na_rt
    开板日 = where[0][0]
    rt.append(开板日)
    if 开板日 == 0:
        print("开板日早于统计日：", code, daily)
        return na_rt
    for day_range in days:
        print("day_range:", day_range)
        截止日 = where[0][0] + day_range
        if 截止日 >= len(daily):
            rt.append(np.nan)
            return na_rt
        # print(开板日)
        # print(截止日)
        区间涨幅 = daily['收盘'][截止日] / daily['收盘'][开板日] - 1
        rt.append(round(区间涨幅, 4))
        # print(区间涨幅)
    return tuple(rt)


df = ak.stock_zh_a_new()[['code', 'name']]
df.columns = ['代码', '简称']
# df = df.head(5)
a = df.apply(lambda c: 开板后区间涨幅(c['代码'], [5, 10, 20]), axis=1, result_type='expand')
print(a)
df[['板数', '5日涨幅', '10日涨幅', '20日涨幅']] = a
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
# print(df)
# df.dropna(inplace=True)
#
# df.to_csv("out/次新股开板后区间涨幅.csv")
# print("开板5日区间涨幅:", df['开板5日区间涨幅'].mean())
# print("开板10日区间涨幅:", df['开板10日区间涨幅'].mean())
# print("开板20日区间涨幅:", df['开板20日区间涨幅'].mean())
