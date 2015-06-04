#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/07 18:15:36 Shin Kanouchi
"""２つのプログラムを作成
train-bigram: 2-gramモデルを学習
test-bigram: 2-gramモデルに基づいて
評価データのエントロピーを計算"""
import argparse
import math
import train01_test


def test_bigram(model_file, test_file):
    H = 0  # エントロピー
    N = 1000000
    lam_start = 0
    lam_end = 100
    lam_step = 5
    w_count = 0
    entropy_dict = {}
    prob_dict = train01_test.import_model(model_file)

    for lam100_1 in range(lam_start, lam_end, lam_step):
        for lam100_2 in range(lam_start, lam_end, lam_step):
            lam_1 = float(lam100_1) / 100
            lam_2 = float(lam100_2) / 100
            for line in open(test_file, 'r'):
                line = line.strip()
                words = line.split()
                words.insert(0, '<s>')
                words.append('</s>')
                for i in range(1, len(words) - 1):
                    unigram = words[i]
                    bigram = '%s %s' % (words[i - 1], words[i])
                    P1 = lam_1 * prob_dict[unigram] + (1 - lam_1) / N
                    P2 = lam_2 * prob_dict[bigram] + (1 - lam_2) * P1
                    H += -math.log(P2, 2)
                    w_count += 1
                    entropy = (float(H) / w_count)
                    entropy_dict["%.2f %.2f" % (lam_1, lam_2)] = entropy
    return entropy_dict


def save_file(entropy_dict, result_file):
    # print 'entropy = %f' % (entropy)
    r_file = open(result_file, "w")
    for lams, ent in sorted(entropy_dict.items(), key=lambda x: x[1]):
        r_file.write("%s\t%.6f\n" % (lams, ent))
        print lams, ent

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test', default="../data/wiki-en-test.word", help='input test data')
    parser.add_argument('-m', '--model', dest='model', default="../output/train02_bigram.model", help='writeing model file')
    parser.add_argument('-r', '--result', dest='result', default="../output/train02_bigram.result", help='writeing result file')
    args = parser.parse_args()
    entropy_dict = test_bigram(args.model, args.test)
    save_file(entropy_dict, args.result)
