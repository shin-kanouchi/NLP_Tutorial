#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/07 22:11:08 Shin Kanouchi
"""
shin:train kanouchishin$ ../script/gradews.pl ../data/wiki-ja-test.word train04.result
Sent Accuracy: 23.81% (20/84)
Word Prec: 71.88% (1943/2703)
Word Rec: 84.22% (1943/2307)
F-meas: 77.56%
Bound Accuracy: 86.30% (2784/3226)
"""
import argparse
import math
import train01_test
from collections import defaultdict


def import_model(model_file):
    prob_dict = defaultdict(lambda: 0)
    for line in open(model_file):
        word, prob = line.strip().split("\t")
        word = unicode(word, 'utf-8')
        prob_dict[word] = float(prob)
    return prob_dict


def back_step(line, best_edge, best_score):
    words = []
    next_edge = best_edge[len(best_edge) - 1]
    while next_edge != 'NULL':
        word = line[next_edge[0]:next_edge[1]]
        words.append(word.encode('utf-8'))
        next_edge = best_edge[next_edge[0]]
    words.reverse()
    return words


def forward_step(line, uni_dict):
    best_edge = {0: 'NULL'}
    best_score = {0: 0}
    for word_end in range(1, len(line) + 1):
        best_score[word_end] = float('inf')
        for word_begin in range(word_end):
            word = line[word_begin:word_end]
            if word in uni_dict or len(word) == 1:
                prob = train01_test.calc_prob(word, uni_dict)
                score_temp = best_score[word_begin] + -math.log(prob)
                if score_temp < best_score[word_end]:
                    print score_temp, word_begin, word_end
                    best_score[word_end] = score_temp
                    best_edge[word_end] = (word_begin, word_end)
    return best_edge, best_score


def word_segment(model_file, test_file, result_file):
    uni_dict = import_model(model_file)
    r_file = open(result_file, "w")
    for line in open(test_file):
        line = unicode(line.strip(), 'utf-8')
        best_edge, best_score = forward_step(line, uni_dict)
        words = back_step(line, best_edge, best_score)
        print ' '.join(words)
        r_file.write(' '.join(words) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', dest='model', default="../output/train04_ja_unigram.model", help='input model data')
    parser.add_argument('-t', '--test', dest='test', default="../data/wiki-ja-test.txt", help='input test data')
    parser.add_argument('-r', '--result', dest='result', default="../output/train04.result", help='writing result file')
    args = parser.parse_args()
    word_segment(args.model, args.test, args.result)
