# -*- coding: utf-8 -*-
"""
@Time ： 2023/9/13 0:06
@Auth ： Philo
@File ：caogao.py
@IDE ：PyCharm
"""

# -*- coding: utf-8 -*-
"""
@Time ： 2023/7/29 16:37
@Auth ： Philo
@File ：匹配时间.py
@IDE ：PyCharm
"""
import pandas as pd
from tqdm import tqdm
#方面级评论
df1 = pd.read_excel("data/方面级：阅读推广.xlsx")
#总评论
df2 = pd.read_excel("data/sorce/一级公共图书馆.xlsx")
#方面级评论
comments = df1.iloc[:,0].tolist()
#总评论
all_comments = df2.iloc[:,0].astype(str).tolist()
print(type(all_comments))
#评论时间
times = df2.loc[:,"times"].tolist()
#图书馆名称
library = df2.loc[:,"图书馆名称"].tolist()
#评论评分
star  = df2.loc[:,"star"].tolist()
#省份
province = df2.loc[:,"省份"]

time = []#方面级短语时间
allc = []#对应的完整评论
lib = []#对应的图书馆
pro = []#对于省份
rank = []#对于评分
for c in tqdm(comments):
    for a in all_comments:
         if c in a:
            time.append(times[all_comments.index(a)])
            lib.append(library[all_comments.index(a)])
            pro.append(province[all_comments.index(a)])
            rank.append(star[all_comments.index(a)])
            allc.append(a)
            break

df = pd.DataFrame({"comments":comments,"完整评论":allc,"时间":time,"评分":rank,"图书馆":lib,"省份":pro})
df.to_excel("data/少儿馆方面级评论.xlsx",index=False)
