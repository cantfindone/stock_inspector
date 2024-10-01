import akshare as ak


def get():
    return ak.stock_yjbb_em(date="20221231")


df =get()

print(df.columns)
df