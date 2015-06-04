#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/07 15:10:54 Shin Kanouchi
import argparse
from collections import defaultdict
"""ファイルの中の単語の頻度を数えるプログラムを作成"""


def main(open_file):
    word_count = defaultdict(lambda: 0)
    for line in open(open_file):
        item = line.strip().split()
        for word in item:
            word_count[word] += 1
    return word_count


def print_dict(word_count):
    for key, value in sorted(word_count.items(), key=lambda x: x[1]):
        print '%s\t%d' % (key, value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test', default="../data/wiki-en-train.word", help='input test data')
    args = parser.parse_args()
    word_count = main(args.test)
    print_dict(word_count)
