import akshare as ak


def get(date=None):
    stock_industry_pe_ratio_cninfo_df = ak.stock_industry_pe_ratio_cninfo(symbol="国证行业分类", date='20220902')
                                                                          # date=str(
                                                                          #     utils.yesterday() if date is None else date))
    stock_industry_pe_ratio_cninfo_df.to_csv("d:\\tmp\industry_pe")
    print(stock_industry_pe_ratio_cninfo_df.head())


if __name__ == "__main__":
    get()
