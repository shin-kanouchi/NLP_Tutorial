#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/15 19:57:51 Shin Kanouchi
import argparse
from collections import defaultdict


def return_sign(i):
    if i >= 0:
        return 1
    else:
        return -1


def predict_one(weight_dict, phi):
    """only predict one thing"""
    score = 0  # score = weight_dict * phi(x)
    for name, value in phi.items():
        if name in weight_dict:
            score += value * weight_dict[name]
    return return_sign(score)


def create_features(x):
    phi = defaultdict(lambda: 0)
    words = x.split()
    for word in words:
        phi['UNI:%s' % (word)] += 1
    return phi


def update_weights(weight_dict, phi, y, c):
    """オンライン学習でL1正則化"""
    for name, value in weight_dict.items():
        if abs(value) < c:
            weight_dict[name] = 0
        else:
            weight_dict[name] -= return_sign(value) * c
    """ここまでオンライン学習"""
    for name, value in phi.items():
        weight_dict[name] += value * y


def train_perceptron(train_file, ITER):
    """マ-ジンを用いたオンライン学習"""
    weight_dict = defaultdict(lambda: 0)
    c = 0.0001
    margin = 1
    for many_iterations in range(1, ITER):
        for line in open(train_file):
            val = 0
            y, x = line.strip().split('\t')
            phi = create_features(x)
            #y2  = predict_one(weight_dict, phi)
            for name, value in phi.items():
                val += weight_dict[name] * value * int(y)
            if val <= margin:
                update_weights(weight_dict, phi, int(y), c)
        print many_iterations
    return weight_dict


def save_file(result_file, weight_dict):
    r_file = open(result_file, "w")
    for k, v in sorted(weight_dict.items(), key=lambda x: x[1]):
        r_file.write("%s\t%f\n" % (k, v))
        print "%s\t%f" % (k, v)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train', dest='train', default="../data/titles-en-train.labeled", help='input training data')
    parser.add_argument('-n', '--num', dest='num_iter', default=20, help='input number of iterations')
    parser.add_argument('-r', '--result', dest='result', default="../output/train09_svm.model", help='writing model file')
    args = parser.parse_args()
    weight_dict = train_perceptron(args.train, args.num_iter)
    save_file(args.result, weight_dict)
