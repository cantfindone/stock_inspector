import datetime
import os
from pathlib import Path

import akshare as ak
import pandas as pd

from finance import utils, finance_indicator, stock_indicator, balance_sheet, cash_flow_yearly, const, cache_manager
from finance.utils import cache


# @cache.memoize(typed=True, expire=const.ONE_HOUR)
def get():
    """
    业绩报告
    :param date: date="20220331"; choice of {"XXXX0331", "XXXX0630", "XXXX0930", "XXXX1231"}; 从 20100331 开始
    :return: df['序号', '股票代码', '股票简称', '每股收益', '营业收入-营业收入', '营业收入-同比增长', '营业收入-季度环比增长',
       '净利润-净利润', '净利润-同比增长', '净利润-季度环比增长', '每股净资产', '净资产收益率', '每股经营现金流量',
       '销售毛利率', '所处行业', '最新公告日期']
    """

    dates = utils.report_dates(2)
    print("dates:", dates)
    performance_file_path = "data/performance"
    latest_report_date = None
    if Path(performance_file_path).exists():
        stock_yjbb_em_df = utils.load_df(performance_file_path)
        stock_yjbb_em_df['最新公告日期'] = pd.to_datetime(stock_yjbb_em_df["最新公告日期"]).dt.date
        latest_report_date = stock_yjbb_em_df['最新公告日期'].max()
        if utils.today() - latest_report_date < datetime.timedelta(hours=12):
            return stock_yjbb_em_df
    report_date = dates[-1].strftime('%Y%m%d')
    print("业绩报表：", report_date)
    stock_yjbb_em_df = ak.stock_yjbb_em(date=report_date)
    # stock_yjbb_em_df = pd.concat([ak.stock_yjbb_em(date=dates[0].strftime('%Y%m%d')),
    #                               ak.stock_yjbb_em(date=dates[1].strftime('%Y%m%d'))])
    stock_yjbb_em_df.sort_values(['最新公告日期'], ascending=False, inplace=True)
    stock_yjbb_em_df.drop_duplicates(subset=['股票代码'], inplace=True)
    stock_yjbb_em_df['最新公告日期'] = pd.to_datetime(stock_yjbb_em_df["最新公告日期"]).dt.date
    # if latest_report_date is not None:
    #     stock_yjbb_em_df[stock_yjbb_em_df['最新公告日期'] >= latest_report_date]['股票代码'].map(
    #         lambda x: utils.clean_stock(x))
    # utils.dump_df(stock_yjbb_em_df, performance_file_path)
    stock_yjbb_em_df['股票代码'].map(lambda c: cache_manager.delete(c, report_date))
    # stock_yjbb_em_df.to_csv("d:\\performance.csv")
    # print(stock_yjbb_em_df)

    return stock_yjbb_em_df


@cache.memoize(typed=True, expire=const.HALF_DAY)
def screen_stocks():
    performance_df = get()
    performance_df = performance_df[
        (performance_df['股票代码'] < '800000')
        & (performance_df['营业收入-同比增长'] > 0)
        & (performance_df['净利润-同比增长'] > 5)
        # & (performance_df['净资产收益率'] > 9)
        & (performance_df['每股经营现金流量'] > 0)
        & (performance_df['股票代码'].str.startswith('4') == False)
        & (performance_df['股票代码'].str.startswith('68') == False)
        ]
    performance_df['finance_indicator'] = performance_df['股票代码'].map(lambda c: finance_indicator.is_good(c))
    performance_df = performance_df[performance_df['finance_indicator']]
    performance_df['dv_ttm'] = performance_df['股票代码'].map(lambda c: stock_indicator.get(c)['dv_ttm'][0])
    performance_df['pe_ttm'] = performance_df['股票代码'].map(lambda c: stock_indicator.get(c)['pe_ttm'][0])
    performance_df['pe_ttm_pctl'] = performance_df['股票代码'].map(
        lambda c: utils.cal_percentile(True, stock_indicator.get(c)['pe_ttm']))
    performance_df['pb'] = performance_df['股票代码'].map(lambda c: stock_indicator.get(c)['pb'][0])
    performance_df['pb_pctl'] = performance_df['股票代码'].map(
        lambda c: utils.cal_percentile(True, stock_indicator.get(c)['pb']))
    performance_df['roe'] = performance_df['pb'] / performance_df['pe_ttm']

    performance_df = performance_df[
        (performance_df['roe'] > 0.18)
        & (performance_df['pe_ttm'] < 25)
        ]

    performance_df['balance_ind'] = performance_df['股票代码'].map(lambda c: balance_sheet.is_good(c))
    performance_df = performance_df[
        performance_df['balance_ind']
    ]
    performance_df['cash_ind'] = performance_df['股票代码'].map(lambda c: cash_flow_yearly.is_good(c))
    performance_df = performance_df[
        performance_df['cash_ind']
    ]

    del performance_df['序号']
    del performance_df['每股收益']
    del performance_df['营业收入-营业收入']
    del performance_df['净利润-净利润']
    del performance_df['每股净资产']
    del performance_df['每股经营现金流量']
    del performance_df['finance_indicator']
    del performance_df['balance_ind']
    del performance_df['最新公告日期']
    performance_df = performance_df.reset_index()
    del performance_df['index']
    return performance_df


if __name__ == "__main__":
    # selected_file_path = "../data/selected"
    #
    # if Path(selected_file_path).exists():
    #     os.remove()
    # selected = []
    # performance = screen_stocks()
    # print(performance.columns)
    # for code in performance['股票代码']:
    #     if finance_indicator.is_good(code):
    #         selected.append(code)
    # utils.dump(selected, selected_file_path)
    # start_time = datetime.date.today()
    # get()
    # end_time = datetime.date.today()
    # print("time cost:", end_time - start_time)
    dates = utils.report_dates(2)
    print(dates)
    df1 = ak.stock_yjbb_em(date=dates[0].strftime('%Y%m%d'))
    print(df1)
