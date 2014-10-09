#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/07 21:50:21 Shin Kanouchi
import argparse
from collections import defaultdict
from train03_train import *

def import_model(model_file):
    weight_dict = {}
    for line in open(model_file):
        ngram, weight = line.strip().split('\t')
        weight_dict[ngram] = float(weight)
    return weight_dict

def predict_all(model_file, test_file, result_file):
    weight_dict = import_model(model_file)     # weight_dict[name] = w_name
    r_file = open(result_file, "w")
    for line in open(test_file):
        phi_dict = create_features(line.strip()) # phi_dict[name] = phi_name(x)
        y_  = predict_one(weight_dict, phi_dict) # sign(weight_dict * phi_dict(x))
        r_file.write('%d\n' % (y_))
        print y_

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', dest='model', default="train03_perceptron.model", help='writeing model file')
    parser.add_argument('-t', '--test', dest='test', default="../data/titles-en-test.word", help='input test data')
    parser.add_argument('-r', '--result', dest='result', default="train03_prediction.result", help='writeing result file')
    args = parser.parse_args()
    predict_all(args.model, args.test, args.result)

"""
shin:train kanouchishin$ ../script/grade-prediction.py ../data/titles-en-test.labeled train03_prediction.result
Accuracy = 90.967056%
"""