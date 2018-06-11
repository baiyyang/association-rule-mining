#!/usr/bin/python
# -*- coding:utf-8 -*-
# **************************
# * Author      :  baiyyang
# * Email       :  baiyyang@163.com
# * Description :  
# * create time :  2018/6/8上午10:30
# * file name   :  apriori.py


min_support = 0.3
min_confidence = 0.5


def loadDataSet(filename):
    """
    加载数据集
    :param filename:
    :return:
    """
    datas = []
    with open(filename, 'r', encoding='utf-8') as fr:
        for line in fr:
            datas.append(line.strip().split(','))
    return datas


def count(items, datas):
    """
    计算items出现在data中的个数
    :param items: list []
    :param datas: list[list] [[]]
    :return:
    """
    num = 0
    for data in datas:
        if set(items).issubset(set(data)):
            num += 1
    return num


def judgeConnect(items1, items2):
    """
    判断两个items是否满足连接步的条件
    :param items1:
    :param items2:
    :return:
    """
    if len(items1) != len(items2):
        return False
    diff = 0
    for item in items1:
        if item not in items2:
            diff += 1
    if diff == 1:
        return True
    else:
        return False


def judgeSame(itemscur, itemsall):
    """
    判断当前的items，是否在之前的集合中出现过
    :param itemscur: list []
    :param itemsall: list[list] [[]]
    :return:
    """
    for items in itemsall:
        if sorted(itemscur) == sorted(items):
            return True
    return False


def getF1(datas):
    """
    得到频繁一项集
    :param datas:
    :return:
    """
    c1 = list(set([item for items in datas for item in items]))
    c1 = [[item] for item in c1]
    f1 = []
    for c in c1:
        if count(c, datas) / float(len(datas)) >= min_support:
            f1.append(c)
    return f1


def getFk(fk_1, datas):
    """
    由频繁k-1项集得到频繁k项集
    :param fk_1: list[list] [[]]
    :param datas: list[list] [[]]
    :return:
    """
    # 得到所有的k项集
    ck = []
    for i in range(len(fk_1)):
        for j in range(i+1, len(fk_1)):
            if judgeConnect(fk_1[i], fk_1[j]):
                items = set(fk_1[i] + fk_1[j])
                if not judgeSame(items, ck):
                    ck.append(list(items))

    # 得到所有的频繁k-1项集
    fk = []
    for items in ck:
        if count(items, datas) / float(len(datas)) >= min_support:
            fk.append(items)
    return fk


if __name__ == "__main__":
    datas = loadDataSet("data")
    f1 = getF1(datas)
    print(f1)
    fk = getFk(f1, datas)
    while len(fk) != 0:
        print(fk)
        fk = getFk(fk, datas)
