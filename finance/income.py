import akshare as ak

from finance import utils
from finance.utils import load_stock, dump_stock


def get(code):
    table = 'income'
    stock_profit_sheet_by_report_em_df = load_stock(table, code)
    if stock_profit_sheet_by_report_em_df is None:
        try:
            stock_profit_sheet_by_report_em_df = ak.stock_profit_sheet_by_report_em(symbol=utils.prefix(code))
            stock_profit_sheet_by_report_em_df = stock_profit_sheet_by_report_em_df[
                ['SECURITY_CODE', 'REPORT_DATE', 'UPDATE_DATE', 'TOTAL_OPERATE_INCOME', 'TOTAL_OPERATE_INCOME_YOY',
                 'OPERATE_INCOME',
                 'OPERATE_INCOME_YOY', 'TOTAL_OPERATE_COST', 'TOTAL_OPERATE_COST_YOY', 'OPERATE_COST',
                 'OPERATE_COST_YOY', 'RESEARCH_EXPENSE',
                 'RESEARCH_EXPENSE_YOY', 'SALE_EXPENSE', 'SALE_EXPENSE_YOY', 'FAIRVALUE_CHANGE_INCOME', 'INVEST_INCOME',
                 'OPERATE_PROFIT', 'OPERATE_PROFIT_YOY'
                    , 'TOTAL_PROFIT', 'TOTAL_PROFIT_YOY', 'NETPROFIT', 'NETPROFIT_YOY'
                    , 'PARENT_NETPROFIT', 'PARENT_NETPROFIT_YOY', 'DEDUCT_PARENT_NETPROFIT',
                 'DEDUCT_PARENT_NETPROFIT_YOY']]
            stock_profit_sheet_by_report_em_df.set_index("REPORT_DATE", inplace=True)
            stock_profit_sheet_by_report_em_df.index.name = None
            stock_profit_sheet_by_report_em_df = stock_profit_sheet_by_report_em_df.head(20)
            stock_profit_sheet_by_report_em_df = stock_profit_sheet_by_report_em_df.iloc[::-1]
            stock_profit_sheet_by_report_em_df['DEDUCT_PARENT_NETPROFIT_Q'] = stock_profit_sheet_by_report_em_df[
                'DEDUCT_PARENT_NETPROFIT'].diff()
            for d in stock_profit_sheet_by_report_em_df.index:
                print(d)
                [year, quarter, day] = d.split(' ')[0].split('-')
                stock_profit_sheet_by_report_em_df.loc[d, 'year'] = year
                stock_profit_sheet_by_report_em_df.loc[d, 'quarter'] = quarter
                if d.find('03-31') > 0:
                    stock_profit_sheet_by_report_em_df.loc[d, 'DEDUCT_PARENT_NETPROFIT_Q'] = \
                        stock_profit_sheet_by_report_em_df.loc[d, 'DEDUCT_PARENT_NETPROFIT']
            stock_profit_sheet_by_report_em_df = stock_profit_sheet_by_report_em_df.iloc[::-1]
            dump_stock(stock_profit_sheet_by_report_em_df, table, code)
        except Exception as e:
            print("except occurred", e)
            print("income_df:", stock_profit_sheet_by_report_em_df)
    # print(stock_profit_sheet_by_report_em_df.head(2))
    # stock_profit_sheet_by_report_em_df.head(2).T.to_csv("d:\\income.csv")
    return stock_profit_sheet_by_report_em_df


def enrich(source_df):
    source_df['扣非同比|环比'] = source_df['id'].map(lambda c: do_enrich(get(c)))


def do_enrich(stock_df):
    return 1 if stock_df[stock_df['quarter'] == stock_df['quarter'][0]]['DEDUCT_PARENT_NETPROFIT_Q'][
                :2].is_monotonic_decreasing else 0, 1 if stock_df['DEDUCT_PARENT_NETPROFIT_Q'][
                                                         :2].is_monotonic_decreasing else 0
