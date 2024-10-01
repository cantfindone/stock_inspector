import akshare as ak

df = ak.stock_history_dividend()
df.sort_values(['累计股息'], inplace=True)
print(df[['代码', '名称', '上市日期', '累计股息', '年均股息']].tail(20))
