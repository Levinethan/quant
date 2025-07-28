import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from statsmodels.tsa import stattools as ts
from statsmodels.graphics.tsaplots import plot_acf
import matplotlib.pyplot as plt
import datetime
from IPython.display import display


size = 1000     ##############  初始成交额变化量  ####################

add_size = 300000    ##############  每次累加的成交额变化量  ####################

baseline = csv_filename+'_'       ############### 保存文件的前缀 ##################

for j in range(1):        ############# 循环次数 ############

    file_name = file_name       ###############  原始数据文件 ############
    df = pd.read_csv(file_name)

    buf_o = []
    buf_h = []
    buf_l = []
    buf_c = []
    buf_v = []
    buf_pos1 = []
    buf_pos2 = []
    buf_b = []
    buf_s = []
    res = []

    pos_sum = 0

    for i in range(0,len(df)):

        # 数据读取
        p_t = df['time'].iloc[i]
        p_o = df['open'].iloc[i]
        p_h = df['high'].iloc[i]
        p_l = df['low'].iloc[i]
        p_c = df['close'].iloc[i]
        p_v = df['volume'].iloc[i]

        #另类数据 taker buy
        p_b = df['buy'].iloc[i]
        p_s = df['sell'].iloc[i]

        di = df.index.values[i]

        # 数据缓存
        buf_o.append(p_o)
        buf_h.append(p_h)
        buf_l.append(p_l)
        buf_c.append(p_c)
        buf_v.append(p_v)
        buf_b.append(p_b)
        buf_s.append(p_s)
        # 累计成交额
        pos_sum = pos_sum + (p_h / p_l) * 1000
        #print("pos_sum : ",pos_sum)

        if pos_sum >= size:

            o = buf_o[0]
            h = max(buf_h)
            l = min(buf_l)
            c = buf_c[-1]
            v = sum(buf_v)
            b = buf_b[0]
            s = buf_s[0]
            p = pos_sum

            res.append({
                'eob': p_t,
                'open': o,
                'high': h,
                'low': l,
                'close': c,
                'buy':b,
                'sell':s,
                'volume': v,
                'pos': p,
                'hang':di
            })

            buf_o.clear()
            buf_h.clear()
            buf_l.clear()
            buf_c.clear()
            buf_v.clear()
            pos_sum = 0

    aaa = pd.DataFrame(res)
    aaa['eob'] = pd.to_datetime(aaa['eob'])
    date = aaa['eob'] > '2024-01-01'   #### 测试集数量

    aaa.to_csv('./temp/' + baseline + str(size) + "_" + str(len(aaa)) + "_" +  str(len(aaa[date])) + ".csv",index = False)


    title_file = baseline + str(size) + "_" + str(len(aaa)) + "_" +  str(len(aaa[date]))
    file_name1 = './temp/' + baseline + str(size) + "_" + str(len(aaa)) + "_" +  str(len(aaa[date])) + ".csv"
    bars = pd.read_csv(file_name1)

    size = size + add_size   ######## 累加  ######


    bars.set_index("eob", inplace=True)

    returns_1 = np.log(bars['close']).diff().dropna()
    returns_2 = np.log(bars['close']).diff(periods=2).dropna()
    returns_3 = np.log(bars['close']).diff(periods=3).dropna()
    returns_4 = np.log(bars['close']).diff(periods=4).dropna()
    returns_5 = np.log(bars['close']).diff(periods=5).dropna()


    standard_1 = (returns_1 - returns_1.mean()) / returns_1.std()
    standard_2 = (returns_2 - returns_2.mean()) / returns_2.std()
    standard_3 = (returns_3 - returns_3.mean()) / returns_3.std()
    standard_4 = (returns_4 - returns_4.mean()) / returns_4.std()
    standard_5 = (returns_5 - returns_5.mean()) / returns_5.std()


    plt.figure(figsize=(16,12))


    sns.kdeplot(standard_1, label="1", color='darkred')
    sns.kdeplot(standard_2, label="2", color='green')
    sns.kdeplot(standard_3, label="3", color='blue')
    sns.kdeplot(standard_4, label="4", color='orange')
    sns.kdeplot(standard_5, label="5", color='magenta')

    sns.kdeplot(np.random.normal(size=1000000), label="Normal", color='black', linestyle="--")

    plt.xticks(range(-5, 6))
    plt.legend(loc=8, ncol=5)
    plt.title(title_file,loc='center', fontsize=20, fontweight="bold", fontname="Times New Roman")
    plt.xlim(-5, 5)
    plt.grid(1)
    plt.show()

    plt.savefig(file_name1 + ".jpg")
    plt.close()
