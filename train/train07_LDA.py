#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/14 12:31:09 Shin Kanouchi

import math
import random
import argparse
from collections import defaultdict


def SampleOne(probs):
    sum_probs = sum(probs)
    remaining = random.uniform(0, sum_probs)
    for i in range(len(probs)):
        remaining -= probs[i]  # 現在の確率を引く
        if remaining <= 0:
            return i
    assert remaining <= 0, "Sample_one should return a value."


def AddCounts(word, topic, docid, amount, xcounts, ycounts):
    topic = str(topic)
    docid = str(docid)
    xcounts[topic] += amount
    ycounts[docid] += amount
    xcounts["%s %s" % (word, topic)] += amount
    ycounts["%s %s" % (topic, docid)] += amount
    return xcounts, ycounts


def first_vectors(import_file, NUM_TOPICS):
    xcorpus = []
    ycorpus = []
    xcounts = defaultdict(lambda: 0)
    ycounts = defaultdict(lambda: 0)
    for line in open(import_file):
        docid = len(xcorpus)
        words = line.strip().split()
        topics = []
        for word in words:
            topic = random.randint(0, NUM_TOPICS - 1)
            topics.append(topic)
            xcounts, ycounts = AddCounts(word, topic, docid, 1, xcounts, ycounts)
        xcorpus.append(words)
        ycorpus.append(topics)
    return xcorpus, ycorpus, xcounts, ycounts


def calc_prob(xcounts, ycounts, i, k, x):
    a = 0.0001
    b = 0.0001
    #トピックkの確率 = P(x|k) * P(k|Y)
    P_xk = (xcounts[x + " " + k] + a) / (xcounts[k] + a)
    P_ky = (ycounts[k + " " + i] + b) / (ycounts[i] + b)
    P = P_xk * P_ky
    return P


def learn_lda(xcorpus, ycorpus, xcounts, ycounts, NUM_TOPICS, ITER):
    for many_iterations in range(1, ITER):
        ll = 0
        for i in range(len(xcorpus)):
            for j in range(len(xcorpus[i])):
                x = xcorpus[i][j]
                y = ycorpus[i][j]
                xcounts, ycounts = AddCounts(x, y, i, -1, xcounts, ycounts)  # カウント減算
                probs = []
                for k in range(0, NUM_TOPICS):
                    P = calc_prob(xcounts, ycounts, str(i), str(k), x)
                    probs.append(P)
                new_y = SampleOne(probs)
                ll += math.log(probs[new_y])  # 対数尤度の計
                xcounts, ycounts = AddCounts(x, new_y, i, 1, xcounts, ycounts)  # カウント加算
                ycorpus[i][j] = new_y
        print ll
    return xcorpus, ycorpus


def save_file(xcorpus, ycorpus, result_file):
    r_file = open(result_file, "w")
    for i in range(len(xcorpus)):
        for j in range(len(xcorpus[i])):
            r_file.write("%s %s\n" % (xcorpus[i][j], ycorpus[i][j]))
            print xcorpus[i][j], ycorpus[i][j]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train', dest='train', default="../data/wiki-en-documents.word", help='input training data')
    parser.add_argument('-n', '--num', dest='num_topics', default=30, help='input number of topics')
    parser.add_argument('-i', '--iter', dest='iter', default=2, help='input number of iterations')
    parser.add_argument('-r', '--result', dest='result', default="../output/train07_LDA.result", help='writing result file')
    args = parser.parse_args()
    xcorpus, ycorpus, xcounts, ycounts = first_vectors(args.train, args.num_topics)
    xcorpus, ycorpus = learn_lda(xcorpus, ycorpus, xcounts, ycounts, args.num_topics, args.iter)
    save_file(xcorpus, ycorpus, args.result)
