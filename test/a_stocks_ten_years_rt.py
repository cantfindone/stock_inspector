from matplotlib import pyplot as plt
from pandas.core.dtypes.common import is_numeric_dtype

from finance import a_stocks, stock_hist_price

plt.clf()
fig = plt.figure()
df = a_stocks.get_gt_10y()
# df['上市时间'] = df['代码'].map(lambda x: stock_info.list_date(x))
print(df.shape)
df['10年涨幅'] = df['代码'].map(lambda x: stock_hist_price.price_diff(x, '20121101', '20221101'))
df['10年涨幅'].plot(kind='kde')
fig.savefig("out/a_stocks_ten_years_rt_kde.jpg", format='jpg')
plt.close(fig)
df.sort_values(['10年涨幅'], inplace=True)
df.loc['mean'] = df.apply(lambda s: round(s.mean(), 2) if is_numeric_dtype(s) else '均值', axis=0)
df.loc['median'] = df.apply(lambda s: round(s.median(), 2) if is_numeric_dtype(s) else '中位数', axis=0)
df.dropna(inplace=True)
df.reset_index(inplace=True)
del df['index']
print(df)
df.to_csv("out/a_stocks_ten_years_rt.csv")
