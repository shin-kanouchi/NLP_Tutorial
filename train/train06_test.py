#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/13 18:52:58 Shin Kanouchi
"""
モデルファイルの作り方
python train02_train.py -r ../data/wiki-ja-train.word -m ../output/train06_lm.model
python train05_train.py -r ../data/wiki-ja-train.pron_word -m ../output/train06_tm.model
精度確認
script/gradekkc.pl data/wiki-ja-test.word output/train06.result
"""
import argparse
import math
import train04_test


def import_tm_model(model_file):
    tm_dict = {}
    for line in open(model_file):
        (T_E, word, pron, prob) = line.strip().split()
        word = word.decode("utf-8")
        pron = pron.decode("utf-8")
        if T_E is "E":
            if pron not in tm_dict:
                tm_dict[pron] = {}
            tm_dict[pron][word] = float(prob)  # tm_dict[しごと][仕事] = 1.000000
    return tm_dict


def get_prob(prev_word, curr_word, lm_dict):
    """Compute smoothed bigram"""
    V = 10000
    l1 = 0.9
    l2 = 0.9
    P1 = l1 * lm_dict[curr_word] + (1 - l1) / V
    P2 = l2 * lm_dict['%s %s' % (prev_word, curr_word)] + (1 - l2) * P1
    return P2


def forward_step(line, lm_dict, tm_dict, line_len):
    best_edge = {0: {"<s>": "NULL"}}
    best_score = {0: {"<s>": 0}}
    for end in range(1, line_len):
        best_score[end] = {}
        best_edge[end] = {}
        for begin in range(end):
            pron = line[begin:end]
            my_tm = {}
            if pron in tm_dict:  # pron =　しごと
                my_tm = tm_dict[pron]  # my_tm = {仕事:0.9, 死事:0.1}
            elif len(pron) == 1:
                my_tm[pron] = 1
            for (curr_word, tm_prob) in my_tm.items():
                for (prev_word, prev_score) in best_score[begin].items():
                    curr_score = prev_score \
                        - math.log(tm_prob * get_prob(prev_word, curr_word, lm_dict))
                    if curr_word not in best_score[end] or curr_score < best_score[end][curr_word]:
                        best_score[end][curr_word] = curr_score
                        best_edge[end][curr_word] = (begin, prev_word)
                        #print begin, end, prev_word, curr_word, curr_score
    # Treat the last step
    best_score[line_len] = {"</s>": float("inf")}
    best_edge[line_len] = {"</s>": ""}
    for (last_word, last_score) in best_score[len(line)].items():
        if last_score < best_score[line_len]["</s>"]:
            best_score[line_len]["</s>"] = last_score
            best_edge[line_len]["</s>"] = (len(line), last_word)
    return best_edge


def backward_step(best_edge, line_len):
    words = []
    next_edge = best_edge[line_len]["</s>"]
    while next_edge != "NULL":
        position, word = next_edge
        words.append(word)
        next_edge = best_edge[position][word]
    words.pop()  # last one is <s>
    words.reverse()
    return words


def test_kkc(lm_file, tm_file, test_file, result_file):
    lm_dict = train04_test.import_model(lm_file)
    tm_dict = import_tm_model(tm_file)
    r_file = open(result_file, "w")
    for line in open(test_file):
        line = line.strip().decode("utf-8")
        line_len = len(line) + 1
        best_edge = forward_step(line, lm_dict, tm_dict, line_len)
        kanji_list = backward_step(best_edge, line_len)
        r_file.write(' '.join(kanji_list).encode("utf-8") + '\n')
        print ' '.join(kanji_list).encode("utf-8")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', dest='model', default="../output/train06_lm.model", help='writing model file')
    parser.add_argument('-n', '--model2', dest='model2', default="../output/train06_tm.model", help='writing model file')
    parser.add_argument('-t', '--test', dest='test', default="../data/wiki-ja-test.pron", help='input test data')
    parser.add_argument('-s', '--result', dest='result', default="../output/train06.result", help='writing result file')
    args = parser.parse_args()
    test_kkc(args.model, args.model2, args.test, args.result)
