import datetime
import math

import akshare as ak

from finance import utils, income, spot_em, const, hist_em, balance_sheet
from finance.utils import cache


def enrich(source_df):
    source_df['roe|pe|price_pctl'] = source_df['id'].map(lambda c: do_enrich(c))


# @cache.memoize(typed=True, expire=const.HALF_DAY)
def do_enrich(c):
    try:
        # pe = spot_em.get(c)['市盈率-动态']
        market_value = spot_em.get(c)['总市值']
        net_profit_de = income.get_indicator(c, 'DEDUCT_PARENT_NETPROFIT_Q', 4)
        pe_ttm_de = market_value / net_profit_de
        hist_price = hist_em.get(c)['收盘']
        equity = balance_sheet.get(c)['TOTAL_EQUITY'][0]
        roe = net_profit_de / equity
        print('market_value of ', c, ":", market_value)
        print('net_profit_de of ', c, ":", net_profit_de)
        print('pe_ttm_de of ', c, ":", pe_ttm_de)
        print('roe of ', c, ":", roe)
        val = min(round((roe * 10), 2), 2), \
              -2 if pe_ttm_de <= 0 else round((25 / pe_ttm_de), 2), \
              round((1 - utils.cal_percentile(True, hist_price)) * 5, 2)
        return val


    except Exception as e:
        print('do_enrich exception in valuation', c, e.__cause__, e, '\n')
        # stock_df.head()[['股票代码', 'roe', 'dv_ttm', 'pe_ttm', 'pb']])
    return 0, 0, 0


if __name__ == "__main__":
    start = datetime.datetime.now()
    print(do_enrich("603619"))
    end = datetime.datetime.now()
    print(end - start)

    # print(ak.stock_a_lg_indicator(symbol='301367'))
    print(income.get_indicator("603619", 'DEDUCT_PARENT_NETPROFIT_Q', 4))
