import akshare as ak


def get():
    df = ak.stock_ggcg_em(symbol="全部")
    return df


if __name__ == "__main__":
    print(get())
