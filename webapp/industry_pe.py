import akshare as ak
import datetime
import finance.utils as utils
date_str = utils.last_trade_day(datetime.date.today()).strftime('%Y%m%d')
pe_df = ak.stock_industry_pe_ratio_cninfo(symbol="国证行业分类", date=date_str)
pe_df = pe_df[pe_df["行业层级"] == 3]
pe_df = pe_df[[
    "变动日期",
    "行业编码",
    "行业名称",
    "公司数量",
    "纳入计算公司数量",
    "总市值-静态",
    "净利润-静态",
    "静态市盈率-加权平均",
    "静态市盈率-中位数",
    "静态市盈率-算术平均",
]].dropna()
pe_df = pe_df.sort_values(["静态市盈率-中位数"]).reset_index(drop=True)
print(pe_df)