import datetime
import os.path
from functools import lru_cache
from io import StringIO
from pathlib import Path

import akshare as ak
import matplotlib
import pandas as pd
import numpy as np
import pickle
import warnings
from diskcache import FanoutCache

warnings.filterwarnings('error')
import pyarrow.parquet

import os

from matplotlib import pyplot as plt
from pandas.core.dtypes.common import is_numeric_dtype

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("stock_inspector\\") + len("stock_inspector\\")]  # stock_inspector，也就是项目的根路径


# dataPath = os.path.abspath(rootPath + 'data\\')


def prefix(code):
    """
    给股票代码加上交易所前缀
    :param code:6位数的股票代码
    :return: 加上交易所前缀的股票代码
    """
    if len(code) != 6:
        raise ValueError("code length ={len(code)}, not equals to 6")
    if (int(code[0])) >= 6:
        return 'sh' + code
    else:
        return 'sz' + code


def today():
    return datetime.date.today()


def yesterday():
    return today() + datetime.timedelta(days=-1)


@lru_cache()
def trade_days():
    for fn in os.listdir("../data"):
        if str(fn).startswith("trade_date_"):
            furthest_date_str = fn[11:]
            furthest_date = datetime.date.fromisoformat(furthest_date_str)
            if furthest_date >= today():
                with open("data" + os.path.sep + fn, 'rb') as file:
                    return pickle.load(file)
            else:
                os.remove("data" + os.path.sep + fn)
    tool_trade_date_hist_sina_df = ak.tool_trade_date_hist_sina()
    trade_dates = tool_trade_date_hist_sina_df['trade_date'].tolist()
    furthest_trade_date = trade_dates[-1]
    # print(furthest_trade_date)
    with open("data" + os.path.sep + f"trade_date_{furthest_trade_date}", 'wb') as file:
        pickle.dump(trade_dates, file)
    return trade_dates


@lru_cache()
def latest_n_trade_days_of(date, n=2):
    """
    返回 日期之前的n个交易日（包含date指定的交易日）
    :param n:
    :param date:
    :return: 交易日期列表（如果date是交易日，将包含date)
    """
    trade_dates = trade_days()
    pop = trade_dates.pop()
    while pop > date:
        pop = trade_dates.pop()
    if pop <= date:
        trade_dates.append(pop)
    return trade_dates[-n:]


@lru_cache()
def last_trade_day(date):
    """
    获取指定日期之前的交易日（不包含指定日期）
    :param date:
    :return: 指定日期之前的交易日（不包含指定日期）
    """
    two_trade_days = latest_n_trade_days_of(date, n=2)
    return two_trade_days[-1] if two_trade_days[-1] < date else two_trade_days[-2]


#
# if __name__ == "__main__":
#     print(today())
#     print(latest_n_trade_days_of(yesterday()))
#     print(last_trade_day(today()))


def clean_stock(code):
    code_path = rootPath + f"data/stocks/{code}"
    if Path(code_path).exists():
        print(f"making dir:{code_path}")
        for fn in os.listdir(code_path):
            os.remove(code_path + '/' + fn)


def dump_stock(df, table, code):
    code_path = rootPath + f"data/stocks/{code}"
    if not Path(code_path).exists():
        print(f"making dir:{code_path}")
        os.mkdir(code_path)
    file_path = code_path + f"/{table}"
    df.to_parquet(file_path)


def load_stock(table, code):
    file_path = rootPath + f"data/stocks/{code}/{table}"
    if Path(file_path).exists():
        return pd.read_parquet(file_path)
    return None


def dump(data, file_path):
    with open(file_path, 'wb') as file:
        return pickle.dump(data, file)


def load(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)


def dump_df(df, file_path):
    return df.to_parquet(file_path)


def load_df(file_path):
    return pd.read_parquet(file_path)


def cal_percentile(is_first_element_target, series):
    if len(series) < 2:
        return 0
    target_value = series.iloc[0] if is_first_element_target else series.iloc[-1]
    series_1 = series.sort_values(ascending=True)
    location = np.where(series_1 == target_value)
    if len(location[0]) > 0:
        #         print(location[0][-1])
        try:
            pctl = round(location[0][-1] / (len(series) - 1), 4)
        except Warning as e:
            print("Warning:", e.__cause__, e, location, series)
    else:
        pctl = -1
    return pctl


matplotlib.rc("font", family='Microsoft YaHei')
matplotlib.use('Agg')


def plot_columns(df, title=''):
    images = []
    if not title == '':
        title = title + '-'
    for c in df.columns.tolist():
        plt.clf()
        fig = plt.figure()
        serial = df[c]
        serial = serial.replace('--', np.nan)
        serial = serial.dropna()
        if len(serial) / len(df) < 1 / 5:
            continue
        try:
            serial = serial.map(lambda x: float(x))
        except Exception as e:
            print("plot excepton in utils", e, serial[-5:])
            continue
        if len(serial) < 30: plt.xticks(range(len(df.index.tolist())), df.index.tolist())
        serial.plot(kind='line', figsize=(22, 10), title=title + c, grid=True)
        img_stringio = StringIO()
        fig.savefig(img_stringio, format='svg')
        images.append({'name': c, 'data': img_stringio.getvalue()})
        plt.close(fig)
    return images


def sum_tuple(tuple_like):
    return sum(tuple_like)


def report_dates(num=2):
    _today = today()
    year = _today.year
    quarter_dates = ["0331", "0630", "0930", "1231"]
    years = [year - 1, year]
    dates = []
    for year in years:
        dates.extend(list(map(lambda x: datetime.date(year, int(x[:2]), int(x[2:])), quarter_dates)))
    for d in range(len(dates)):
        dd = len(dates) - d - 1
        if dates[dd] < _today:
            return dates[dd - 1:dd + 1]
    return dates


cache = FanoutCache(directory=rootPath + "data")

if __name__ == "__main__":
    print(report_dates(2)[0].strftime("%Y%m%d"))
