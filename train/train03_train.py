#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/07 21:14:24 Shin Kanouchi

import argparse
from collections import defaultdict


def predict_one(weight_dict, phi_dict):
    score = 0
    for name, value in phi_dict.items():
        if name in weight_dict:
            score += value * weight_dict[name]
    if score >= 0:
        return 1
    else:
        return -1


def create_features(text):
    phi_dict = defaultdict(lambda: 0)
    words = text.split()
    for word in words:
        phi_dict['UNI:%s' % (word)] += 1
    return phi_dict


def update_weights(weight_dict, phi_dict, y):
    for name, value in phi_dict.items():
        weight_dict[name] += value * y


def train_perceptron(train_file):
    weight_dict = defaultdict(lambda: 0)
    for line in open(train_file):
        y, text = line.strip().split('\t')
        phi_dict = create_features(text)
        y_ = predict_one(weight_dict, phi_dict)
        print y_, y
        if y_ != int(y):
            update_weights(weight_dict, phi_dict, int(y))
    return weight_dict


def save_file(model_file, weight_dict):
    m_file = open(model_file, "w")
    for k, v in sorted(weight_dict.items(), key=lambda x: x[1]):
        m_file.write('%s\t%f\n' % (k, v))
        print '%s\t%f' % (k, v)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--train', dest='train', default="../data/titles-en-train.labeled", help='input training data')
    parser.add_argument('-m', '--model', dest='model', default="../output/train03_perceptron.model", help='writeing model file')
    args = parser.parse_args()
    w_dict = train_perceptron(args.train)
    save_file(args.model, w_dict)
