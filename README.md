# auto binning 分箱工具

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

####  基于最大woe分裂分箱

    df = pd.read_csv('credit_old.csv')
    df = df[['Age','target']]
    df = df.dropna()

    t = splitBywoe(df['Age'], df['target'])
    t.fit(trend='up',minwoe=0.11)
    print(t.bins) # [16. 25. 42. 50. 52. 54. 63. 67. 72. 94.]
    t.fit(trend='up', num_split=4)
    print(t.bins) # [16. 25. 29. 33. 36. 94.]
