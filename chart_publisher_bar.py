import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
from dbc_chart import Chart

chart = Chart()
results = chart.publisher_count()

def publisher_chart():
    publisher = []
    count = []
    for result in results:
        publisher.append(result[3])
        count.append(result[4])
      # pandasでデータ処理
    columns =["publisher","count"]
    df = pd.DataFrame(columns=columns)
    df['publisher'] = publisher
    df['count'] = count
    # 棒グラフを描く
    left=df['publisher']
    height = df['count']
    plt.figure(dpi=100, figsize=(4.5,3))
    plt.bar(left, height)
    plt.xticks(rotation=270)
    plt.tight_layout()
    plt.savefig("image/publisher_bar_chart.png")


if __name__ == '__main__':

  publisher_chart() 