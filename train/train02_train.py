#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/07 17:40:22 Shin Kanouchi

import argparse
from collections import defaultdict
"""2 つのプログラムを作成
train-bigram: 2-gram モデルを学習
test-bigram: 2-gram モデルに基づいて評価データのエントロピーを計算"""

def train_bigram(train_file):
    word_count  = defaultdict(lambda:0)
    context_count = defaultdict(lambda:0)
    for line in open(train_file):
        word = line.strip().split(' ')
        word.insert(0, '<s>')
        word.append('</s>')
        for i in range(1, len(word) - 1):
            bigram = '%s %s' % (word[i-1], word[i])
            word_count[bigram]       += 1
            context_count[word[i-1]] += 1
            word_count[word[i]]      += 1
            context_count['']        += 1
    return word_count, context_count

def save_file(word_count, context_count, model_file):
    m_file = open(model_file, "w")
    for ngram, count in sorted(word_count.items(), key = lambda x: x[1]):
        words = ngram.split(' ')
        if len(words) > 1:
            context = words[0]
        else:
            context = ''
        prob = float(word_count[ngram]) / context_count[context]
        print ngram, prob
        m_file.write('%s\t%.6f\n' % (ngram, prob))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--train', dest='train', default="../data/wiki-en-train.word", help='input training data')
    parser.add_argument('-m', '--model', dest='model', default="train02_bigram.model", help='writeing model file')
    args = parser.parse_args()
    word_count, context_count= train_bigram(args.train)
    save_file(word_count, context_count, args.model)