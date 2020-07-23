# -*- coding: utf-8 -*-
import math


class Node(object):
    def __init__(self, char):
        self.char = char
        self.word_finish = False
        self.count = 0
        self.child = []
        self.isback = False

class TrieNode(object):
    def __init__(self, node, data=None, PMI_limit=20):
        self.root = Node(node)
        self.PMI_limit = PMI_limit
        if not data:
            return
        node = self.root
        for key, values in data.items():
            new_node = Node(key)
            new_node.count = int(values)
            new_node.word_finish = True
            node.child.append(new_node)

    def add(self, word):
        node = self.root
        for count, char in enumerate(word):
            found_in_child = False
            for child in node.child:
                if char == child.char:
                    node = child
                    found_in_child = True
                    break

            if not found_in_child:
                new_node = Node(char)
                node.child.append(new_node)
                node = new_node

            if count == len(word) - 1:
                node.count += 1
                node.word_finish = True

        length = len(word)
        node = self.root
        if length == 3:
            word = list(word)
            word[0], word[1], word[2] = word[1], word[2], word[0]

            for count, char in enumerate(word):
                found_in_child = False
                if count != length - 1:
                    for child in node.child:
                        if char == child.char:
                            node = child
                            found_in_child = True
                            break
                else:
                    for child in node.child:
                        if char == child.char and child.isback:
                            node = child
                            found_in_child = True
                            break
                if not found_in_child:
                    new_node = Node(char)
                    node.child.append(new_node)
                    node = new_node

                if count == len(word) - 1:
                    node.count += 1
                    node.isback = True
                    node.word_finish = True

    def search_one(self):
        result = {}
        node = self.root
        if not node.child:
            return False, 0

        total = 0
        for child in node.child:
            if child.word_finish is True:
                total += child.count

        for child in node.child:
            if child.word_finish is True:
                result[child.char] = child.count / total
        return result, total

    def search_bi(self):
        result = {}
        node = self.root
        if not node.child:
            return False, 0

        total = 0
        # 1 grem 各词的占比，和 1 grem 的总次数
        one_dict, total_one = self.search_one()
        for child in node.child:
            for ch in child.child:
                if ch.word_finish is True:
                    total += ch.count

        for child in node.child:
            for ch in child.child:
                if ch.word_finish is True:
                    # 互信息值越大，说明 a,b 两个词相关性越大
                    PMI = math.log(max(ch.count, 1), 2) - math.log(total, 2) - math.log(one_dict[child.char],
                                                                                        2) - math.log(one_dict[ch.char],
                                                                                                      2)
                    # 这里做了PMI阈值约束
                    if PMI > self.PMI_limit:
                        # 例如: dict{ "a_b": (PMI, 出现概率), .. }
                        result[child.char + '_' + ch.char] = (PMI, ch.count / total)
        return result

    def search_left(self):
        result = {}
        node = self.root
        if not node.child:
            return False, 0

        for child in node.child:
            for cha in child.child:
                total = 0
                p = 0.0
                for ch in cha.child:
                    if ch.word_finish is True and ch.isback:
                        total += ch.count
                for ch in cha.child:
                    if ch.word_finish is True and ch.isback:
                        p += (ch.count / total) * math.log(ch.count / total, 2)
                # 计算的是信息熵
                result[child.char + cha.char] = -p
        return result

    def search_right(self):
        result = {}
        node = self.root
        if not node.child:
            return False, 0

        for child in node.child:
            for cha in child.child:
                total = 0
                p = 0.0
                for ch in cha.child:
                    if ch.word_finish is True and not ch.isback:
                        total += ch.count
                for ch in cha.child:
                    if ch.word_finish is True and not ch.isback:
                        p += (ch.count / total) * math.log(ch.count / total, 2)
                # 计算的是信息熵
                result[child.char + cha.char] = -p
        return result

    def find_word(self, N):
        # 通过搜索得到互信息
        # 例如: dict{ "a_b": (PMI, 出现概率), .. }
        bi = self.search_bi()
        # 通过搜索得到左右熵
        left = self.search_left()
        right = self.search_right()
        result = {}
        for key, values in bi.items():
            d = "".join(key.split('_'))
            # 计算公式 score = PMI + min(左熵， 右熵) => 熵越小，说明越有序，这词再一次可能性更大！
            result[key] = (values[0] + min(left[d], right[d])) * values[1]

        # 按照 大到小倒序排列，value 值越大，说明是组合词的概率越大
        # result变成 => [('世界卫生_大会', 0.4380419441616299), ('蔡_英文', 0.28882968751888893) ..]
        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        print("result: ", result)
        dict_list = [result[0][0]]
        # print("dict_list: ", dict_list)
        add_word = {}
        new_word = "".join(dict_list[0].split('_'))
        # 获得概率
        add_word[new_word] = result[0][1]

        # 取前5个
        # [('蔡_英文', 0.28882968751888893), ('民进党_当局', 0.2247420989996931), ('陈时_中', 0.15996145099751344), ('九二_共识', 0.14723726297223602)]
        for d in result[1: N]:
            flag = True
            for tmp in dict_list:
                pre = tmp.split('_')[0]
                # 新出现单词后缀，再老词的前缀中 or 如果发现新词，出现在列表中; 则跳出循环 
                # 前面的逻辑是： 如果A和B组合，那么B和C就不能组合(这个逻辑有点问题)，例如：`蔡_英文` 出现，那么 `英文_也` 这个不是新词
                # 疑惑: **后面的逻辑，这个是完全可能出现，毕竟没有重复**
                if d[0].split('_')[-1] == pre or "".join(tmp.split('_')) in "".join(d[0].split('_')):
                    flag = False
                    break
            if flag:
                new_word = "".join(d[0].split('_'))
                add_word[new_word] = d[1]
                dict_list.append(d[0])

        return result, add_word
