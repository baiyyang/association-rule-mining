#!/usr/bin/python
# -*- coding:utf-8 -*-
# **************************
# * Author      :  baiyyang
# * Email       :  baiyyang@163.com
# * Description :  
# * create time :  2018/6/8上午10:30
# * file name   :  apriori.py


import itertools


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
    s1 = []  # 支持度
    for c in c1:
        support = count(c, datas) / float(len(datas))
        if support >= min_support:
            f1.append(c)
            s1.append(support)
    return f1, s1


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
    sk = []
    for items in ck:
        support = count(items, datas) / float(len(datas))
        if support >= min_support:
            fk.append(items)
            sk.append(support)
    return fk, sk


def generate_fk(datas):
    """
    生成频繁项集
    :param datas:
    :return:
    """
    f_s = {}
    f1, s1 = getF1(datas)
    for f, s in zip(f1, s1):
        f_s[frozenset(f)] = s
    fk, sk = getFk(f1, datas)
    while fk:
        for f, s in zip(fk, sk):
            f_s[frozenset(f)] = s
        fk, sk = getFk(fk, datas)
    return f_s


def generate_rule(f_s):
    """
    由频繁项集生成规则
    :param f_s:
    :return:
    """
    rules = []
    for key, value in f_s.items():
        if len(key) >= 2:
            rules.extend(rule(key, f_s, []))
    return rules


def rule(items, f_s, cur_rule):
    for item in itertools.combinations(items, 1):
        if items - frozenset(item) in f_s.keys() and \
                f_s[items] / f_s[items - frozenset(item)] >= min_confidence:
            cur_rule.append((str([items - frozenset(item)]), str(item),
                             f_s[items] / float(f_s[items - frozenset(item)])))
            rule(items - frozenset(item), f_s, cur_rule)
    return cur_rule


if __name__ == "__main__":
    datas = loadDataSet("data")
    f_s = generate_fk(datas)
    print("频繁项集：{} 个".format(len(f_s)))
    for key, value in f_s.items():
        print("{} : {:.2f}".format(key, value))
    rules = generate_rule(f_s)
    print("关联规则：{}个".format(len(rules)))
    for reason, result, conf in rules:
        print("{} ----> {} : {}".format(reason, result, conf))
