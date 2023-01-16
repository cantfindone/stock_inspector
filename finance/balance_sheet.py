import datetime

import akshare as ak
import pandas as pd

from finance import utils, income, const
from finance.utils import cache


def get(code):
    key = 'balance_sheet' + code

    df = cache.get(key)
    if df is not None and 'GOODWILL' not in df.columns:
        df = None
        print("delete balance_sheet cache!", code, cache.delete(key))

    if df is None:
        df = ak.stock_balance_sheet_by_report_em(symbol=utils.prefix(code))
        if len(df) == 0:
            return None
        # print(df.head())
        try:
            df = df[
                ['SECURITY_CODE', 'REPORT_DATE', 'UPDATE_DATE', 'ACCOUNTS_RECE', 'NOTE_ACCOUNTS_RECE',
                 'CONTRACT_LIAB', 'INVENTORY', 'GOODWILL', 'INTANGIBLE_ASSET', 'FIXED_ASSET', 'CIP', 'TOTAL_EQUITY',
                 'TOTAL_LIAB_EQUITY', 'TOTAL_LIABILITIES']].head(20)
        except Exception as e:
            print("exception in get balance_sheet", e, code)
            df = df[
                ['SECURITY_CODE', 'REPORT_DATE', 'UPDATE_DATE', 'GOODWILL', 'INTANGIBLE_ASSET',
                 'FIXED_ASSET', 'CIP', 'TOTAL_EQUITY', 'TOTAL_LIAB_EQUITY', 'TOTAL_LIABILITIES'
                 ]].head(20)
        df[df.columns[3:]] = df[df.columns[3:]].astype(float)
        df = df.fillna(0)
        now = datetime.datetime.now()
        days = (pd.to_datetime(df['REPORT_DATE'])[0] +datetime.timedelta(days=(90 if now.month < 12 else 180)) - now).days
        days = max(days, 5)
        cache.set(key, df, expire=const.ONE_DAY * days, tag=code)
    return df


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


# @cache.memoize(typed=True, expire=const.HALF_DAY)
def do_enrich(code):
    df = get(code)
    has_contract_liab = True
    if df is None:
        print("no balance_sheet for stock:", code)
        return 0, 0, 0, 0
    if 'CONTRACT_LIAB' not in df.columns:
        print("no CONTRACT_LIAB in balance_sheet", code)
        has_contract_liab = False
    try:
        contract_liab = False
        if has_contract_liab:
            df['CONTRACT_LIAB'] = df['CONTRACT_LIAB'].astype(float)
            contract_liab = df['CONTRACT_LIAB'][:2].is_monotonic_decreasing
        goodwill = df['GOODWILL'][0]
        fixed_asset = df['FIXED_ASSET'][0]
        total_equity = df['TOTAL_EQUITY'][0]
        operate_income_q = income.get_indicator(code, 'OPERATE_INCOME_Q')
        return 1 if contract_liab else 0, \
               0 if not has_contract_liab or operate_income_q == 0 else round(min(
                   df['CONTRACT_LIAB'][0] / operate_income_q, 1), 1) * 5, \
               round(1 - goodwill / total_equity, 2), \
               round(1 - fixed_asset / total_equity, 2)

    except Exception as e:
        print("is good exception in balance_sheet", e, code, df)
        return 0, 0, 0, 0


def enrich(source_df):
    source_df['负债|商誉|固定'] = source_df['id'].map(lambda c: do_enrich(c))


if __name__ == "__main__":
    start = datetime.datetime.now()
    df = get("000001")
    print('GOODWILL' in df.columns)
    end = datetime.datetime.now()
    print(end - start)
    # print(ak.stock_balance_sheet_by_report_em(symbol=utils.prefix('601688')).head(2).to_csv('balance_sheet.csv'))
