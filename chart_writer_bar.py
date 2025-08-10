import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from dbc_chart import Chart

chart = Chart()
results = chart.writer_count()

def writer_chart():
    writers = []
    count = []
    for result in results:
        writers.append(result[3])
        count.append(result[4])
      # pandasでデータ処理
    columns =["writer","count"]
    df = pd.DataFrame(columns=columns)
    df['writer'] = writers
    df['count'] = count
    # 棒グラフを描く
    left=df['writer']
    height = df['count']
    plt.figure(dpi=100, figsize=(4.5,3))
    plt.bar(left, height)
    plt.xticks(rotation=270)
    plt.tight_layout()
    plt.savefig("image/writer_bar_chart.png")


if __name__ == '__main__':

  writer_chart()    