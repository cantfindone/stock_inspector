from django.urls import path

from . import views, list_views, ir_views, account_views,indicator_views, balance_views,cashflow_views,cash_revenue_views,income_views,holding_views,zygc_views,industry_views
from django.contrib.staticfiles.views import serve
from .views import StockCreateView
app_name = 'webapp'
urlpatterns = [
    path('favicon.ico', serve, {'path': 'webapp/images/favicon.ico'}),
    path('', views.index, name='index'),
    path('stock/holding', holding_views.lists, name='holding'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('ir', ir_views.plot, name='ir'),
    path('account', account_views.plot, name='account'),
    path('stock', list_views.score_boad, name='stock'),
    path('stock/low_pb_pctl', list_views.low_pb_pctl, name='low_pb_pctl'),
    path('stock/<str:id>/<str:name>/add', StockCreateView.as_view, name='add'),
    path('stock/<str:code>/<str:name>/stock_indicator', indicator_views.indicator, name='stock_indicator'),
    path('stock/<str:code>/<str:name>/stock_indicator_plot', indicator_views.plot, name='stock_indicator_plot'),
    path('stock/<str:code>/<str:name>/finance_indicator_plot', indicator_views.plot_finance, name='finance_indicator_plot'),
    path('stock/<str:code>/<str:name>/balance', balance_views.get, name='balance'),
    path('stock/<str:code>/<str:name>/balance_plot', balance_views.plot, name='balance_plot'),
    path('stock/<str:code>/<str:name>/cash', cashflow_views.get, name='cash'),
    path('stock/<str:code>/<str:name>/cash_plot', cashflow_views.plot, name='cash_plot'),
    path('stock/<str:code>/<str:name>/cash_revenue_plot', cash_revenue_views.plot, name='cash_revenue_plot'),
    path('stock/<str:code>/<str:name>/income', income_views.get, name='income'),
    path('stock/<str:code>/<str:name>/income_plot', income_views.plot, name='income_plot'),
    path('stock/<str:code>/<str:name>/zygc', zygc_views.get, name='zygc'),
    path('stock/<str:code>/<str:name>/zygc_plot', zygc_views.plot, name='zygc_plot'),
    path('industry', industry_views.industries, name='industry'),
    path('industry/<str:code>/<str:name>', industry_views.members, name='members'),
    path('industry/<str:code>/<str:name>/plot', industry_views.plot, name='iplot'),
    # path('stock', stock_views.fetch, name='fetch'),
]
