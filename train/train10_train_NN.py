#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/19 23:28:46 Shin Kanouchi

import math
import random
import argparse
from collections import defaultdict


def create_features(x):
    phi = defaultdict(lambda: 0)
    words = x.split()
    for word in words:
        phi['UNI:%s' % (word)] += 1
    return phi


def make_network():
    network = []
    for i in range(node):
        if i == node - 1:
            layer = 2
            weight_dict = defaultdict(lambda: 0)
        else:
            layer = 1
            weight_dict = defaultdict(lambda: random.uniform(-0.01, 0.01))
        network.append((layer, weight_dict))
    return network


def predict_one(weight_dict, phi):
    score = 0
    for name, value in phi.items():
        if name in weight_dict:
            score += value * weight_dict[name]
    return math.tanh(score)


def predict_nn(network, phi):
    y = [phi, {}, {}]  # 各層の値
    for i in range(node):
        layer, weight = network[i]
        answer = predict_one(weight, y[layer - 1])  # 前の層の値に基づいて計算
        y[layer][i] = answer  # 次の層に計算された値を保存
    return y


def update_nn(network, phi, yy):
    delta = []
    lam = 0.5
    k = 1
    for i in range(node):
        delta.append(0)
    y = predict_nn(network, phi)  # calculate y using predict_nn
    for j in range(node - 1, -1, -1):  # each node j in reverse order:
        layer = network[j][0]
        if j == node - 1:  # is the last node:
            delta[j] = yy - y[2][2]
        else:
            right_node = len([n for n in network if n[0] == layer + 1])
            # print "right_node" ,right_node
            for i in range(right_node):
                # print y[layer-1][j], delta[j+k+i], network[j+k+i][1][i]
                delta[j] += (1 - y[layer][j] * y[layer][j]) * delta[j + k + i] * network[j + k + i][1][i]
            # print "delta[j]",delta[j]
        k += 1
        if network[j][0] != network[j - 1][0]:
            k = 1
    for j in range(node):
        layer, w = network[j]
        for name, val in y[layer - 1].items():
            w[name] += lam * delta[j] * val
        network[j] = (layer, w)
    return network


def train_perceptron(train_file, ITER):
    network = make_network()
    for many_iterations in range(1, ITER):
        for line in open(train_file):
            y, x = line.strip().split('\t')
            phi = create_features(x)
            network = update_nn(network, phi, int(y))
    return network


def print_train(network, model_file):
    layer, weight_dict = network[2]
    for k, v in sorted(weight_dict.items(), key=lambda x: x[1]):
        print '%s\t%s' % (str(k), str(v))
    print layer, len(network)


def test_perceptron(network, test_file):
    for x in open(test_file):
        phi = create_features(x)
        y = predict_nn(network, phi)
        if y[-1][node - 1] >= 0:
            pass
            #print 1
        else:
            pass
            #print -1

if __name__ == '__main__':
    node = 3
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train', dest='train', default="../data/titles-en-train.labeled", help='input training data')
    parser.add_argument('-e', '--test', dest='test', default="../data/titles-en-test.word", help='input test data')
    parser.add_argument('-m', '--model', dest='model', default="../output/train10_NN.model", help='writing model file')
    parser.add_argument('-r', '--result', dest='result', default="../output/train10_NN.result", help='writing result file')
    parser.add_argument('-n', '--num', dest='num_iter', default=5, help='input number of iterations')
    args = parser.parse_args()
    network = train_perceptron(args.train, args.num_iter)
    print_train(network, args.model)
    test_perceptron(network, args.test)
