#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/08 16:53:28 Shin Kanouchi

import argparse
from collections import defaultdict

def train_hmm(train_file):
    for line in open(train_file):
        words = line.strip().split()
        words.insert(0, "<s>_<s>")
        words.append("</s>_</s>")
        pre_tag = ""
        for word_tag in words:
            word,tag = word_tag.split("_")
            # タグのユニグラムカウント
            tag_dict[tag] += 1
            emit_dict[tag+" "+word] += 1
            # タグのバイグラムカウント
            if pre_tag is not "":
                trans_dict[pre_tag+" "+tag] +=1
            pre_tag = tag

def save_file(model_file):
    m_file = open(model_file, "w")
    for key, value in sorted(emit_dict.items()):
        m_file.write('E %s %f\n' % (key, value/tag_dict[key.split()[0]]))
        print "E", key, value/tag_dict[key.split()[0]]
    for key, value in sorted(trans_dict.items()):
        m_file.write('T %s %f\n' % (key, value/tag_dict[key.split()[0]]))
        print "T", key, value/tag_dict[key.split()[0]]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--train', dest='train', default="../data/wiki-en-train.norm_pos", help='input model data')
    parser.add_argument('-m', '--model', dest='model', default="../output/train05_hmm.model", help='writeing model file')
    args = parser.parse_args()
    trans_dict = defaultdict(lambda:.0)
    emit_dict  = defaultdict(lambda:.0)
    tag_dict   = defaultdict(lambda:.0)
    train_hmm(args.train)
    save_file(args.model)
