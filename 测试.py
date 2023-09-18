# -*- coding: utf-8 -*-
"""
@Time ： 2023/7/30 12:14
@Auth ： Philo
@File ：测试.py
@IDE ：PyCharm
"""
# 导入相关库
import jieba # 中文分词库
import numpy as np # 数学计算库
from sklearn.feature_extraction.text import CountVectorizer # 词频向量化库
from sklearn.metrics.pairwise import cosine_similarity # 余弦相似度计算库
import pandas as pd
from tqdm import tqdm

# 定义输入参数
data = pd.read_excel(r"C:\Users\18079\Desktop\少儿馆.xlsx")
# D = data['comments'].apply(str).tolist() # 评论语料集合
D = ["这是第一句,这是第二句。。。。体验太差了，服务态度不好，无语；而且还没有指示牌。",
     "这是第一句,这是第二句、环境很好，很安静，夏天空调很足，带孩子去孩子很开心，停车算比较方便，经常去打卡",
     "带孩子来图书馆参加小队活动，图书馆的书很多。",
     "黄建筑，蓝玻璃，不规则几何结构，外表看起来一副卡通的样子，这就是福建省少年儿童图书馆。图书馆的门前停着一辆“馆车”，有各楼层的总指引，保安看见我带着相机，告诫我进去了可不能拍照。建筑共五层，电梯有箱式和观光两种，可能是专为少儿设计，运行略慢。每层楼均有几部自助借还机，小朋友们排队操作，秩序俨然。有家长等候区，配大大的软沙发，一看就挺舒服。还有游乐区，写着“玩具已经消毒”，图书也这么标着，不过，书标上没有加保护膜。哈哈镜和秋千椅是不可少的，此外还有电子书。周四闭馆。图书馆每月印制一份“公益活动计划”，4A硬纸，四个版面，列出时间地点主讲人等信息，预告的活动有讲座。阅读指导。论坛、展演、主题展览、阅读推广、义工培训，我数了一下，整个5月共有22个活动，涉及的主题有国学、",
     "福建省少年儿童图书馆位于福州市鼓楼区东街28号，地处市中心繁华路段，交通便捷。于2011年9月26日正式开馆服务。新馆实际用地面积17938平方米，建筑由国内知名设计师设计，主体有如彩色的积木块，活泼有趣，突出少年儿童图书馆的特色。少年儿童图书馆的服务对象范围广，能满足学龄前幼儿到高中学生和教育教学工作者及家长的学习阅读需要。现有馆内能容纳60万册文献，阅读座位1000余个，是青少年完美的第二课堂。为了丰富少年儿童的课外生活，除了基本的图书、音像借阅室和多媒体阅览室，我馆还增设视障儿童阅览区、玩具游乐区、动漫体验区、幼儿专业教室、家长借阅区等特色馆室。我们还特别为少年儿童及家长们策划了各式各样引人入胜的活动和讲座，围绕少年儿童的兴趣爱好、成长需求、各种知识，"] # 测试语料
Wl = 3 # 向左搜索最大窗口
Wr = 2 # 向右搜索最大窗口，相对于3
P = ["。","！","？","，","；","、","：",".",",","~","."] # 短句切割标点符号
P_tilde = ["：","；","。",] # 方面级上下文切割标点符号
T = ["活动"] # 方面词词库，
thres = 0.6 # 去重阈值

# 定义输出参数
S_prime = [] # 候选方面级语句列表

# Step1：抽取候选方面级语句集合。
print("Step1：抽取候选方面级语句集合。")
save_list = []
for di in tqdm(D): # 遍历评论语料集合D 中每一条评论di
    s_list = [] # 存储短句列表
    start = 0 # 短句起始位置
    for i in range(len(di)): # 遍历评论中的每个字符
        if di[i] in P: # 如果字符是短句切割标点符号
            s_list.append(di[start:i+1]) # 切分短句并加入列表
            start = i+1 # 更新短句起始位置
    Idx = [] # 存储索引值列表
    for j in range(len(s_list)): # 遍历短句列表中的每个短句
        for t in T: # 遍历方面词词库中的每个方面词
            if t in s_list[j]: # 如果方面词出现在短句中
                Idx.append(j) # 将索引值j存入列表Idx
                break # 跳出内层循环
    for j in Idx: # 遍历索引列表Idx中的每个索引值j
        SL = s_list[:j] # 将评论di切分为左搜索区间SL
        SR = s_list[j+1:] # 将评论di切分为右搜索区间SR
        k = 1 # 初始化向左搜索步长k
        while k <= Wl and k <= len(SL): # 当k不超过向左搜索最大窗口和左搜索区间长度时
            if SL[-k][-1] in P_tilde: # 如果sj-k末尾字符为标点集P_title中的标点符号
                break # 停止遍历并跳出循环
            k += 1 # 否则增加向左搜索步长k
        l = 0 # 初始化向右搜索步长l
        while l < Wr and l < len(SR): # 当l不超过向右搜索最大窗口和右搜索区间长度时
            if SR[l][-1] in P_tilde: # 如果sj+l末尾字符为标点集P_tilde中的标点符号
                break # 停止遍历并跳出循环
            l += 1 # 否则增加向右搜索步长l
        if k !=1:
            s = "".join(SL[-k+1:] + [s_list[j]] + SR[:l+1]) # 将sj-k+1到sj+l拼接为方面级语句
        else:
            s = "".join([s_list[j]] + SR[:l+1])
        # print(SR)
        print(l,s)
        # print(s)
        S_prime.append(s) # 将方面级语句存入候选语句列表S_prime
        save_list.extend(s_list)

# Step2：删除重复语句，获取方面级语句列表。
print("Step2：删除重复语句，获取方面级语句列表。")
vectorizer = CountVectorizer() # 初始化词频向量化器
X = vectorizer.fit_transform(S_prime) # 将候选语句列表转化为词频矩阵
X = X.toarray() # 将词频矩阵转化为数组
for i in tqdm(range(len(S_prime))): # 遍历候选语句列表中的每个语句si
    for j in range(i+1, len(S_prime)): # 遍历候选语句列表中的每个语句sj
        Simij = cosine_similarity(X[i].reshape(1,-1), X[j].reshape(1,-1)) # 计算两条语句的余弦相似度
        if Simij > thres: # 如果余弦相似度大于阈值thres
            if len(S_prime[i]) > len(S_prime[j]): # 如果si比sj长
                S_prime[j] = "" # 从S_prime中删除sj
            else: # 否则
                S_prime[i] = "" # 从S_prime中删除si

# 输出经过去重后的方面级语句列表S_prime
S_prime = [s for s in S_prime if s != ""] # 去除空字符串


