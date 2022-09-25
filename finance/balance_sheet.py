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
                 'CONTRACT_LIAB',  'INVENTORY']]
        except:
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
        contract_liab = df['CONTRACT_LIAB'][:2].is_monotonic_decreasing
        return contract_liab or df['CONTRACT_LIAB'][0] > df['ACCOUNTS_RECE'][0] * 0.5
    except:
        print(code, df)
        return False


def enrich(source_df):
    source_df['合同负债'] = source_df['id'].map(lambda c: 1 if is_good(c) else 0)
