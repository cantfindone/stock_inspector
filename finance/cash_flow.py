import akshare as ak

from finance import utils
from finance.utils import load_stock, dump_stock


def get(code):
    table = 'cash_flow'
    stock_cash_flow_sheet_by_report_em_df = load_stock(table, code)
    if stock_cash_flow_sheet_by_report_em_df is None:
        try:
            stock_cash_flow_sheet_by_report_em_df = ak.stock_cash_flow_sheet_by_yearly_em(symbol=utils.prefix(code))
            stock_cash_flow_sheet_by_report_em_df = stock_cash_flow_sheet_by_report_em_df[
                ['SECURITY_CODE', 'REPORT_DATE', 'NETCASH_FINANCE', 'NETCASH_FINANCE_YOY',
                 'NETCASH_INVEST',
                 'NETCASH_INVEST_YOY', 'NETCASH_OPERATE', 'NETCASH_OPERATE_YOY', 'NETPROFIT', 'NETPROFIT_YOY']]
            stock_cash_flow_sheet_by_report_em_df.set_index("REPORT_DATE", inplace=True)
            stock_cash_flow_sheet_by_report_em_df.index.name = None
            dump_stock(stock_cash_flow_sheet_by_report_em_df, table, code)
        except Exception as e:
            print("get cash_flow_df exception:", e, stock_cash_flow_sheet_by_report_em_df)
    # print(stock_cash_flow_sheet_by_report_em_df.head(2))
    # stock_cash_flow_sheet_by_report_em_df.head(2).T.to_csv("d:\\cash_flow.csv")
    return stock_cash_flow_sheet_by_report_em_df


def is_good(code):
    df = get(code)
    if df is None:
        return False
    # if 'CONTRACT_LIAB' not in df.columns.tolist():
    #     return True
    try:
        df = df.iloc[:5, ::]
        # return df['NETCASH_OPERATE'].sum() > df['NETCASH_INVEST'].sum()
        return df['NETCASH_FINANCE'].mean() < df['NETCASH_OPERATE'].mean() * 0.1 and df['NETCASH_OPERATE'].mean() > 0
    except Exception as e:
        print("is good except in cash_flow", e, code, df)
        return False


def enrich(source_df):
    source_df['cash_flow'] = source_df['id'].map(lambda c: 1 if is_good(c) else 0)
