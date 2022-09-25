from functools import lru_cache

import akshare as ak
import matplotlib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from finance.utils import dump_stock, load_stock


# @lru_cache
def get(code):
    """

    :param code:
    :return: df['日期', '摊薄每股收益(元)', '加权每股收益(元)', '每股收益_调整后(元)', '扣除非经常性损益后的每股收益(元)',
       '每股净资产_调整前(元)', '每股净资产_调整后(元)', '每股经营性现金流(元)', '每股资本公积金(元)',
       '每股未分配利润(元)', '调整后的每股净资产(元)', '总资产利润率(%)', '主营业务利润率(%)', '总资产净利润率(%)',
       '成本费用利润率(%)', '营业利润率(%)', '主营业务成本率(%)', '销售净利率(%)', '股本报酬率(%)',
       '净资产报酬率(%)', '资产报酬率(%)', '销售毛利率(%)', '三项费用比重', '非主营比重', '主营利润比重',
       '股息发放率(%)', '投资收益率(%)', '主营业务利润(元)', '净资产收益率(%)', '加权净资产收益率(%)',
       '扣除非经常性损益后的净利润(元)', '主营业务收入增长率(%)', '净利润增长率(%)', '净资产增长率(%)',
       '总资产增长率(%)', '应收账款周转率(次)', '应收账款周转天数(天)', '存货周转天数(天)', '存货周转率(次)',
       '固定资产周转率(次)', '总资产周转率(次)', '总资产周转天数(天)', '流动资产周转率(次)', '流动资产周转天数(天)',
       '股东权益周转率(次)', '流动比率', '速动比率', '现金比率(%)', '利息支付倍数', '长期债务与营运资金比率(%)',
       '股东权益比率(%)', '长期负债比率(%)', '股东权益与固定资产比率(%)', '负债与所有者权益比率(%)',
       '长期资产与长期资金比率(%)', '资本化比率(%)', '固定资产净值率(%)', '资本固定化比率(%)', '产权比率(%)',
       '清算价值比率(%)', '固定资产比重(%)', '资产负债率(%)', '总资产(元)', '经营现金净流量对销售收入比率(%)',
       '资产的经营现金流量回报率(%)', '经营现金净流量与净利润的比率(%)', '经营现金净流量对负债比率(%)', '现金流量比率(%)',
       '短期股票投资(元)', '短期债券投资(元)', '短期其它经营性投资(元)', '长期股票投资(元)', '长期债券投资(元)',
       '长期其它经营性投资(元)', '1年以内应收帐款(元)', '1-2年以内应收帐款(元)', '2-3年以内应收帐款(元)',
       '3年以内应收帐款(元)', '1年以内预付货款(元)', '1-2年以内预付货款(元)', '2-3年以内预付货款(元)',
       '3年以内预付货款(元)', '1年以内其它应收款(元)', '1-2年以内其它应收款(元)', '2-3年以内其它应收款(元)',
       '3年以内其它应收款(元)']
    """
    table = 'finance_indicator'
    stock_financial_analysis_indicator_df = load_stock(table, code)
    if stock_financial_analysis_indicator_df is None:
        stock_financial_analysis_indicator_df = ak.stock_financial_analysis_indicator(symbol=code)
        if stock_financial_analysis_indicator_df is not None:
            dump_stock(stock_financial_analysis_indicator_df, table, code)
    # stock_financial_analysis_indicator_df.to_csv("d:\\finance_indicator.csv")
    return stock_financial_analysis_indicator_df[[
        '日期', '销售毛利率(%)', '销售净利率(%)', '净资产报酬率(%)', '资产报酬率(%)', '主营利润比重', '净资产收益率(%)'
        , '主营业务收入增长率(%)', '应收账款周转天数(天)', '存货周转天数(天)',
        '资产负债率(%)', '经营现金净流量对销售收入比率(%)', '经营现金净流量与净利润的比率(%)']][:20]


def is_good(code):
    df = get(code)
    try:
        inventory_turnover_days = df['存货周转天数(天)'][:2].is_monotonic_increasing
        account_receivable_turnover_days = df['应收账款周转天数(天)'][:2].is_monotonic_increasing
        operation_cashflow_profit_ratio = df['经营现金净流量与净利润的比率(%)'][:2].is_monotonic_decreasing
        return inventory_turnover_days and (
                operation_cashflow_profit_ratio or df['经营现金净流量与净利润的比率(%)'][1] > 95)
    except:
        print(code, df)
        return False


def do_enrich(code):
    df = get(code)
    inventory_turnover_days = df['存货周转天数(天)'][:2].is_monotonic_increasing
    account_receivable_turnover_days = df['应收账款周转天数(天)'][:2].is_monotonic_increasing
    ivnt = inventory_turnover_days or float(df['存货周转天数(天)'][0]) < 60 or float(
        df['存货周转天数(天)'][0]) < pd.to_numeric(df['存货周转天数(天)'].replace('--', np.nan)).quantile(.3)
    accnt = account_receivable_turnover_days or float(df['应收账款周转天数(天)'][0]) < 60 or float(
        df['应收账款周转天数(天)'][0]) < pd.to_numeric(df['应收账款周转天数(天)'].replace('--', np.nan)).quantile(.3)
    return 1 if ivnt else 0, 1 if accnt else 0


def enrich(source_df):
    source_df['存货|应收'] = source_df['id'].map(lambda c: do_enrich(c))


if __name__ == "__main__":
    # for f in FontManager().ttflist:
    #     print(f.name)

    matplotlib.rc("font", family='Microsoft YaHei')
    sheet = get("603501")

    print(sheet.columns)
    sheet.set_index('日期', inplace=True)
    inttd = sheet['存货周转天数(天)'].replace('--', np.nan).apply(lambda x: float(x))
    print(inttd)

    inttd = inttd.interpolate()  # Filling in NaN in a Series via linear interpolation.
    print(inttd)
    inttd = inttd[::-1]
    inttd.plot(kind='bar', figsize=(10, 5))
    plt.show()

    print(is_good('603501'))