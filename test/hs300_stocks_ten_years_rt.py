from pandas.core.dtypes.common import is_numeric_dtype

from finance import a_stocks, stock_hist_price, index_stock_hist, stock_info

df = index_stock_hist.get('sh000300')
df = df[(df['in_date'] < '2012-11-01') & (df['out_date'] > '2012-11-01')]
df.drop_duplicates(inplace=True)
df.reset_index(inplace=True)
del df['index']
df.columns = ['代码', '入选时间', '出选时间']
print(df['代码'])
stock_name = df['代码'].map(lambda x: stock_info.name(x))
df.insert(1, '名称', stock_name)
# df['上市时间'] = df['代码'].map(lambda x: stock_info.list_date(x))
print(df.shape)
df['10年涨幅'] = df['代码'].map(lambda x: stock_hist_price.price_diff(x, '20121101', '20221101'))
df.sort_values(['10年涨幅'], inplace=True)
df.loc['mean'] = df.apply(lambda s: round(s.mean(), 2) if is_numeric_dtype(s) else '-', axis=0)
df.dropna(inplace=True)
df.reset_index(inplace=True)
del df['index']
print(df)
df.to_csv("out/hs300_stocks_ten_years_rt.csv")
