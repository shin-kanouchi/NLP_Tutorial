#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/08 22:34:05 Shin Kanouchi

import argparse
from collections import defaultdict

def train_hmm(train_file):
    all_dict   = defaultdict(lambda:.0)
    for line in open(train_file):
        words = line.strip().split()
        words.insert(0, "<s>_<s>")
        words.append("</s>_</s>")
        pre_tag = ""
        for word_tag in words:
            word,tag = word_tag.split("_")
            all_dict[tag] += 1 # タグのカウント
            if word != '<s>' and word != '</s>':
                all_dict["E "+tag+" "+word] += 1
            if pre_tag is not "":
                all_dict["T "+pre_tag+" "+tag] +=1
            pre_tag = tag
    return all_dict

def save_file(model_file , all_dict):
    m_file = open(model_file, "w")
    for key, value in sorted(all_dict.items()):
        items = key.split()
        if len(items) == 3:
            T_E, k1, k2 = items
        else: continue
        m_file.write('%s %s %s %f\n' % (T_E, k1, k2, value/all_dict[k1]))
        print '%s %s %s %f' % (T_E, k1, k2, value/all_dict[k1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--train', dest='train', default="../data/wiki-en-train.norm_pos", help='input model data')
    parser.add_argument('-m', '--model', dest='model', default="train05_hmm2.model", help='writeing model file')
    args = parser.parse_args()
    all_dict = train_hmm(args.train)
    save_file(args.model, all_dict)