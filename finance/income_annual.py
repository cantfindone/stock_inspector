import akshare as ak

from finance import utils


def get(code):
    stock_profit_sheet_by_yearly_em = ak.stock_profit_sheet_by_yearly_em(symbol=utils.prefix(code))
    # print(stock_profit_sheet_by_yearly_em.head(2))
    stock_profit_sheet_by_yearly_em.head(2).to_csv("d:\\tmp\income.csv")
    sheet = stock_profit_sheet_by_yearly_em[
        ['SECURITY_CODE', 'REPORT_DATE', 'UPDATE_DATE', 'TOTAL_OPERATE_INCOME', 'TOTAL_OPERATE_INCOME_YOY', 'OPERATE_INCOME',
         'OPERATE_INCOME_YOY', 'TOTAL_OPERATE_COST', 'TOTAL_OPERATE_COST_YOY', 'OPERATE_COST', 'OPERATE_COST_YOY', 'RESEARCH_EXPENSE',
         'RESEARCH_EXPENSE_YOY', 'SALE_EXPENSE', 'SALE_EXPENSE_YOY', 'FAIRVALUE_CHANGE_INCOME', 'INVEST_INCOME', 'OPERATE_PROFIT', 'OPERATE_PROFIT_YOY'
            , 'TOTAL_PROFIT', 'TOTAL_PROFIT_YOY', 'NETPROFIT', 'NETPROFIT_YOY'
            , 'PARENT_NETPROFIT', 'PARENT_NETPROFIT_YOY', 'DEDUCT_PARENT_NETPROFIT', 'DEDUCT_PARENT_NETPROFIT_YOY']]
    return sheet


