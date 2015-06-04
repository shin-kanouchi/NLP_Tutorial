#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/07 16:11:34 Shin Kanouchi
"""2つのプログラムを作成
train-unigram: 1-gram モデルを学習
test-unigram: 1-gram モデルを読み込み、
エントロピーとカバレージを計算"""
import argparse
import math
from collections import defaultdict


def import_model(model_file):
    prob_dict = defaultdict(lambda: 0)
    for line in open(model_file):
        word, prob = line.strip().split("\t")
        prob_dict[word] = float(prob)
    return prob_dict


def calc_prob(word, prob_dict):
    N = 10 ** 6
    lambda_1 = .95
    lambda_unk = 1 - lambda_1
    prob = lambda_unk / N
    if word in prob_dict:
        prob += lambda_1 * prob_dict[word]
    return prob


def test_unigram(model_file, test_file):
    H = 0  # エントロピー
    unk = 0  # 未知語
    w_count = 0
    prob_dict = import_model(model_file)
    for line in open(test_file, "r"):
        words = line.strip().split()
        words.append("</s>")
        for word in words:
            P = calc_prob(word, prob_dict)
            H += -math.log(P, 2)
            print H, '/', w_count
            w_count += 1
            if word not in prob_dict:
                unk += 1

    print "entropy  = %f" % (float(H) / w_count)
    print "coverage = %f" % (float(w_count - unk) / w_count)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test', default="../data/wiki-en-test.word", help='input test data')
    parser.add_argument('-m', '--model', dest='model', default="../output/train01_unigram.model", help='writeing model file')
    args = parser.parse_args()
    test_unigram(args.model, args.test)
