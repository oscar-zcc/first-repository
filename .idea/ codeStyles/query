import tushare as ts
import pandas as pd
# 全部股票列表
def stock_all_data():
    df = ts.get_stock_basics()
    return df
# data = stock_all_data()
# a = data['name'] == '闰土股份'
# print(data[a])
def stock_now_all(code):
    df = ts.get_realtime_quotes(code)
    return df
print(stock_now_all('002440'))
def stock_k_data(code):
    df = ts.get_hist_data(code)
    # 导出到csv文件中
    outputpath = '/home/tarena/aid1907/data_analyze/try_analysis/k_data.csv'
    df.to_csv(outputpath, sep=',', index=True, header=True)
    return df
print(stock_k_data('600352'))
# def stock_new_data():
#     df = ts.pro_api().new_share()
#     return df
# print(stock_new_data())

