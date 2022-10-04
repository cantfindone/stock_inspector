from functools import lru_cache

import akshare as ak

from finance import utils
from finance.utils import load_stock, dump_stock


# @lru_cache
def get(code):
    table = 'balance_sheet'
    stock_balance_sheet_by_report_em_df = load_stock(table, code)
    if stock_balance_sheet_by_report_em_df is None:
        stock_balance_sheet_by_report_em_df = ak.stock_balance_sheet_by_report_em(symbol=utils.prefix(code))
        if len(stock_balance_sheet_by_report_em_df) == 0:
            return None
        print(stock_balance_sheet_by_report_em_df.head())
        try:
            stock_balance_sheet_by_report_em_df = stock_balance_sheet_by_report_em_df[
                ['SECURITY_CODE', 'REPORT_DATE', 'UPDATE_DATE', 'ACCOUNTS_RECE',
                 'CONTRACT_LIAB', 'INVENTORY']]
        except Exception as e:
            print("exception in get balance_sheet", e, code)
            stock_balance_sheet_by_report_em_df = stock_balance_sheet_by_report_em_df[
                ['SECURITY_CODE', 'REPORT_DATE', 'UPDATE_DATE', 'ACCOUNTS_RECE'
                 ]]
        dump_stock(stock_balance_sheet_by_report_em_df, table, code)
    return stock_balance_sheet_by_report_em_df


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


def do_enrich(code):
    df = get(code)
    if df is None:
        print("no balance_sheet for stock:", code)
        return 0, 0
    if 'CONTRACT_LIAB' not in df.columns.tolist():
        print("no CONTRACT_LIAB in balance_sheet", code)
        return 0, 0
    try:
        df['CONTRACT_LIAB'] = df['CONTRACT_LIAB'].astype(float)
        contract_liab = df['CONTRACT_LIAB'][:2].is_monotonic_decreasing
        return 2 if contract_liab else 0, 1 if df['CONTRACT_LIAB'][0] > df['ACCOUNTS_RECE'][0] else 0
    except Exception as e:
        print("is good exception in balance_sheet", e, code, df)
        return 0, 0


def enrich(source_df):
    source_df['负债|应收'] = source_df['id'].map(lambda c: do_enrich(c))
