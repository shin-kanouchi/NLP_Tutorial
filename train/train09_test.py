#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/15 20:17:40 Shin Kanouchi

import argparse
import train03_test

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', dest='model', default="../output/train09_svm.model", help='writing model file')
    parser.add_argument('-t', '--test', dest='test', default="../data/titles-en-test.word", help='input test data')
    parser.add_argument('-r', '--result', dest='result', default="../output/train09_svm.result", help='writing result file')
    args = parser.parse_args()
    train03_test.predict_all(args.model, args.test, args.result)