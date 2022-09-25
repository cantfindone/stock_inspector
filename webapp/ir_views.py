import matplotlib
import matplotlib.pyplot as plt
from akshare import rate_interbank
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg

matplotlib.rc("font", family='Microsoft YaHei')


def plot(request):
    df = rate_interbank(market="上海银行同业拆借市场", symbol="Shibor人民币", indicator="3月")
    df.set_index("报告日", inplace=True)
    print(df.head())
    plt.clf()
    fig = plt.figure()
    df['利率'].plot(kind='line', figsize=(24, 12), title="上海银行同业拆借市场3月期利率", grid=True)
    canvas = FigureCanvasAgg(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    plt.close(fig)
    return response
