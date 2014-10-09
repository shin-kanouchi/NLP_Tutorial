#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/07 15:44:50 Shin Kanouchi

import argparse
from collections import defaultdict
"""2つのプログラムを作成
train-unigram: 1-gram モデルを学習
test-unigram: 1-gram モデルを読み込み、エントロピーとカバレージを計算"""

def train_unigram(train_file):
    word_count  = defaultdict(lambda:0)
    for line in open(train_file):
        item = line.strip().split()
        item.append("</s>")
        for word in item:
            word_count[word]          += 1
            word_count['TOTAL_count'] += 1
    return word_count

def save_file(word_count, model_file):
    m_file = open(model_file, "w")
    for k, v in word_count.items():
        prob = float(word_count[k]) / word_count['TOTAL_count']
        print k, prob
        m_file.write("%s\t%f\n" % (k, prob))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train', dest='train', default="../data/wiki-en-train.word", help='input training data')
    parser.add_argument('-m', '--model', dest='model', default="train01_unigram.model", help='writeing model file')
    args = parser.parse_args()
    word_count = train_unigram(args.train)
    save_file(word_count, args.model)