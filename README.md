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

### 向前迭代方法 (forward method)

    # load data
    df = pd.read_csv('credit_old.csv')
    df = df[['Age','target']]
    df = df.dropna()
    
#### 基于最大woe分裂分箱

在得到尽可能细粒度的细分箱之后，寻找上下分箱woe差异最大的初始切割点，并得到woe趋势，之后迭代找到下一个woe差异最大且趋势相同的切割点，直到满足woe差异不大于一个阈值或分箱数（切割点数）满足要求

    t = forwardSplit(df['Age'], df['target'])
    t.fit(sby='woe',minv=0.01,init_split=20)
    print(t.bins) # [16. 25. 29. 33. 36. 38. 40. 42. 44. 46. 48. 50. 52. 54. 55. 58. 60. 63. 72. 94.]
    t = forwardSplit(df['Age'], df['target'])
    t.fit(sby='woe',num_split=4,init_split=20)
    print(t.bins) # [16. 42. 44. 48. 50. 94.]
    woe_dict = {}
    for i in range(len(t.bins)-1):
        v = t.value[(t.x < t.bins[i+1]) & (t.x >= t.bins[i])]
        woe = t._cal_woe(v)
        woe_dict[(t.bins[i], t.bins[i+1])] = woe
    print(woe_dict)
    # {(16.0, 25.0): 0.11373232830301286, (25.0, 42.0): 0.07217546872710079, (42.0, 50.0): 0.04972042405868509, (50.0, 72.0): -0.07172614369435065, (72.0, 94.0): -0.13778318584223453}

![avatar](https://github.com/kaiwang0112006/autoBinning/blob/master/doc/woe1.JPG)
![avatar](https://github.com/kaiwang0112006/autoBinning/blob/master/doc/woe2.JPG)

#### 基于最大iv分裂分箱

与最大woe分裂分箱方法类似，在得到尽可能细粒度的细分箱之后，寻找iv值最大的切割点，并得到woe趋势，之后迭代找到下一个iv最大且woe趋势相同的切割点，直到分箱数（切割点数）满足要求

    # sby='woeiv'时考虑woe趋势，sby='iv'时不考虑woe趋势
    t = forwardSplit(df['Age'], df['target'])
    t.fit(sby='iv',minv=0.1,init_split=20)
    print(t.bins) # [16. 25. 29. 33. 36. 38. 40. 42. 44. 46. 48. 50. 58. 60. 63. 94.]
    t = forwardSplit(df['Age'], df['target'])
    t.fit(sby='iv',num_split=4,init_split=20)
    print(t.bins) # [16. 25. 33. 36. 38. 94.]
    t.fit(sby='woeiv',num_split=4,init_split=20)
    print(t.bins) # [16. 25. 33. 36. 38. 94.]
    
### 向后迭代方法 (backward method)

#### 基于最大iv合并分箱

迭代每次删除一个分箱切点，是去掉后整体iv最大

    t = backwardSplit(df['Age'], df['target'])
    t.fit(sby='iv',num_split=5)
    print(t.bins) # [16.  17.5 18.5 85.5 95. ]
