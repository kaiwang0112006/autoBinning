# auto binning 分箱工具

## 安装

    pip install autoBinning

## 基础工具 (simpleMethods)

    my_list = [1,1,2,2,2,2,3,3,4,5,6,7,8,9,10,10,20,20,20,20,30,30,40,50,60,70,80,90,100]
    my_list_y = [1,1,2,2,2,2,1,1,1,2,2,2,1,1]
    t = simpleMethods(my_list)
    t.equalSize(3)
    # 每个分箱样本数平均
    print(t.bins) # [  1.           5.33333333  20.         100.        ]
    # 等间距划分分箱
    t.equalValue(4)
    print(t.bins) # [  1.    25.75  50.5   75.25 100.  ]
    # 基于numpy histogram分箱
    t.equalHist(4)
    print(t.bins) # [  1.    25.75  50.5   75.25 100.  ]

## 基于标签的有监督自动分箱

#### 基于最大woe分裂分箱

按照等距等频分箱（每个分箱样本量相同）得到潜在切分点，计算每个切分点上下的woe，寻找最大的woe变化切分点，

    df = pd.read_csv('credit_old.csv')
    df = df[['Age','target']]
    df = df.dropna()

    t = trendSplit(df['Age'], df['target'])
    t.fit(sby='woe',minv=0.01,init_split=20,trend='up')
    print(t.bins) # [16. 25. 42. 50. 63. 72. 94.]
    t.fit(sby='woe',num_split=4,init_split=20,trend='up')
    print(t.bins) # [16. 25. 42. 50. 72. 94.]

![avatar](https://github.com/kaiwang0112006/autoBinning/blob/master/doc/woe1.JPG)
![avatar](https://raw.githubusercontent.com/kaiwang0112006/clusfps/master/guild.png)

#### 基于最大iv分裂分箱

    df = pd.read_csv('credit_old.csv')
    df = df[['Age','target']]
    df = df.dropna()

    t = splitByiv(df['Age'], df['target'])
    t.fit(miniv=0.1)
    print(t.bins) # [16.  18.5 82.5 83.5 84.5 85.5 86.5 95. ]
    t = trendSplit(df['Age'], df['target'])
    t.fit(sby='iv',minv=0.1)
    print(t.bins) # [16.  18.5 82.5 83.5 84.5 85.5 86.5 95. ]
    t = trendSplit(df['Age'], df['target'])
    t.fit(sby='iv',minv=0.1,init_split=20)
    print(t.bins) # [16. 25. 29. 33. 36. 38. 40. 42. 46. 48. 50. 94.]
    t = trendSplit(df['Age'], df['target'])
    t.fit(sby='iv',num_split=4,init_split=20)
    print(t.bins) # [16. 25. 29. 33. 42. 94.]
