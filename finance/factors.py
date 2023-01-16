from finance import finance_indicator, cash_flow_quarter, balance_sheet, stock_indicator, income_quarter, income
from finance.utils import sum_tuple


def enrich_data(df):
    # print(df)
    finance_indicator.enrich(df)
    cash_flow_quarter.enrich(df)
    balance_sheet.enrich(df)
    stock_indicator.enrich(df)
    income.enrich(df)

    df['score'] = df['存货|应收|天数|净利率'].apply(sum_tuple) \
                  + df['负债|商誉|固定'].apply(sum_tuple) \
                  + df['扣非同比|环比'].apply(sum_tuple) \
                  + df['roe|dv|pe|pepctl|pbpctl'].apply(sum_tuple) \
                  + df['融资|营收现金率'].apply(sum_tuple)
    df.sort_values(['score'], inplace=True, ascending=False)
    df.reset_index(inplace=True)
    del df['index']
    return df


def enrich_bank_data(df):
    # print(df)
    finance_indicator.enrich(df)
    stock_indicator.enrich(df)
    income.enrich(df)
    df['score'] = df['roe|dv|pe|pepctl|pbpctl'].apply(sum_tuple) + df['扣非同比|环比'].apply(sum_tuple)
    df.sort_values(['score'], inplace=True, ascending=False)
    df.reset_index(inplace=True)
    del df['index']
    return df
