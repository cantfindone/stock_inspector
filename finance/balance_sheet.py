import akshare as ak

from finance import utils, income, const
from finance.utils import load_stock, dump_stock, cache


@cache.memoize(typed=True, expire=const.HALF_DAY)
def get(code):
    table = 'balance_sheet'
    stock_balance_sheet_by_report_em_df = load_stock(table, code)
    if stock_balance_sheet_by_report_em_df is None:
        stock_balance_sheet_by_report_em_df = ak.stock_balance_sheet_by_report_em(symbol=utils.prefix(code))
        if len(stock_balance_sheet_by_report_em_df) == 0:
            return None
        # print(stock_balance_sheet_by_report_em_df.head())
        try:
            stock_balance_sheet_by_report_em_df = stock_balance_sheet_by_report_em_df[
                ['SECURITY_CODE', 'REPORT_DATE', 'UPDATE_DATE', 'ACCOUNTS_RECE', 'NOTE_ACCOUNTS_RECE',
                 'CONTRACT_LIAB', 'INVENTORY']]
        except Exception as e:
            print("exception in get balance_sheet", e, code)
            stock_balance_sheet_by_report_em_df = stock_balance_sheet_by_report_em_df[
                ['SECURITY_CODE', 'REPORT_DATE', 'UPDATE_DATE', 'ACCOUNTS_RECE'
                 ]]
        dump_stock(stock_balance_sheet_by_report_em_df, table, code)
        stock_balance_sheet_by_report_em_df[stock_balance_sheet_by_report_em_df.columns[3:]] = \
            stock_balance_sheet_by_report_em_df[stock_balance_sheet_by_report_em_df.columns[3:]].astype(float)
    return stock_balance_sheet_by_report_em_df.fillna(0)

@cache.memoize(typed=True, expire=const.HALF_DAY)
def is_good(code):
    df = get(code)
    if df is None:
        return False
    if 'CONTRACT_LIAB' not in df.columns.tolist():
        return True
    try:
        df['CONTRACT_LIAB'] = df['CONTRACT_LIAB'].astype(float)
        contract_liab = df['CONTRACT_LIAB'][:2].is_monotonic_decreasing
        return contract_liab or df['CONTRACT_LIAB'][0] > df['ACCOUNTS_RECE'][0]
    except Exception as e:
        print("is good exception in balance_sheet", e, code, df)
        return False

@cache.memoize(typed=True, expire=const.HALF_DAY)
def do_enrich(code):
    df = get(code)
    if df is None:
        print("no balance_sheet for stock:", code)
        return 0, 0, 0
    if 'CONTRACT_LIAB' not in df.columns.tolist():
        print("no CONTRACT_LIAB in balance_sheet", code)
        return 0, 0, 0
    try:
        df['CONTRACT_LIAB'] = df['CONTRACT_LIAB'].astype(float)
        contract_liab = df['CONTRACT_LIAB'][:2].is_monotonic_decreasing
        accounts_rece_ = df['ACCOUNTS_RECE'][0]
        operate_income_q = income.get_indicator(code, 'OPERATE_INCOME_Q')
        return 1 if contract_liab else 0, 0 if accounts_rece_ == 0 else min(
            round(df['CONTRACT_LIAB'][0] / accounts_rece_, 2),
            1), 0 if operate_income_q == 0 else round(min(
            df['CONTRACT_LIAB'][0] / operate_income_q, 1), 1) * 10
    except Exception as e:
        print("is good exception in balance_sheet", e, code, df)
        return 0, 0, 0


def enrich(source_df):
    source_df['负债|应收'] = source_df['id'].map(lambda c: do_enrich(c))


if __name__ == "__main__":
    print(ak.stock_balance_sheet_by_report_em(symbol=utils.prefix("600519")).columns.tolist())
