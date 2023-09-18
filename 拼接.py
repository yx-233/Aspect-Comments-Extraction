# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/31 15:23
@Auth ： Philo
@File ：拼接.py
@IDE ：PyCharm
"""
# 导入pandas模块
import pandas as pd
import os
# 定义文件根目录
root = "C:\\Users\\18079\\Desktop\\workspace\\少儿馆"
# 获取目录下的所有excel文件名
files = pd.Series(os.listdir(root))

# 筛选出以.xlsx结尾的文件名
files = files[files.str.endswith(".xlsx")]
# 定义一个空的数据框用于存储拼接后的数据
df_list = [ ]
# 遍历每个文件名
for file in files:
    # 读取文件内容
    data = pd.read_excel(root + "\\" + file)
    # 增加一列library，值为文件名去掉.xlsx后缀
    data["library"] = file[:-5]
    # 将数据追加到df中
    df_list.append(data)
# 输出拼接后的数据
df = pd.concat(df_list)

df.to_excel("C:\\Users\\18079\\Desktop\\少儿馆.xlsx",index=False)