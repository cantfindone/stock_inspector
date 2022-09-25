import akshare as ak


def get():
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    return stock_zh_a_spot_em_df[['代码', '名称']]
    # print(stock_zh_a_spot_em_df)


if __name__ == "__main__":
    get()
