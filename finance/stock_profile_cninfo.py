import akshare as ak

stock_profile_cninfo_df = ak.stock_profile_cninfo(symbol="600030")
print(stock_profile_cninfo_df.T)