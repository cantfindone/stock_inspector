import akshare as ak

stock_fhps_detail_em_df = ak.stock_fhps_detail_em(symbol="300073")
print(stock_fhps_detail_em_df[['报告期','除权除息日','现金分红-股息率']])