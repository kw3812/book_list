from matplotlib.style import library
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from dbc_chart import Chart

chart = Chart()
results = chart.all_count()
print(type(results))
def union_chart():
    book = results[0][0]
    disp = results[1][0]
    book_counts = dict(library = book,Disposal = disp)
    # pandasでデータ処理
    columns =["book","count"]
    df = pd.DataFrame(columns=columns)
    df['book'] = book_counts.keys()
    df['count'] = book_counts.values()
    # 円グラフを描く
    label = df['book']
    data = df['count']
    plt.figure(dpi=100, figsize=(4.5,3))
    plt.pie(data, labels=label, counterclock=False, startangle=90, autopct="%.1f%%", pctdistance=0.5)
    plt.savefig("image/chart_disp_pi.png")

if __name__ == '__main__':

  union_chart() 
