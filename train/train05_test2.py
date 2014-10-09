#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/09 03:16:36 Shin Kanouchi

import argparse
import math
from collections import defaultdict

def import_model(model_file):
    for line in open(model_file):
        item = line.strip().split()
        if item[0] is "T":
            trans_dict[item[1]+" "+item[2]] = float(item[3])
            tag_dict[item[1]] = 1
            tag_dict[item[2]] = 1
        else:
            emit_dict[item[1]+" "+item[2]]  = float(item[3])
            vocab[item[2]]    = 1

def forward_step(best_score, best_edge, words):
    for i in range(len(words)):
        for prev_tag in tag_dict.keys():
            for next_tag in tag_dict.keys():
                i_prev    = '%s %s' % (i, prev_tag)
                prev_next = '%s %s' % (prev_tag, next_tag)
                next_word = '%s %s' % (next_tag, words[i])
                if i_prev in best_score and prev_next in trans_dict:
                    if next_word not in emit_dict:
                        vocab[words[i]] = 1
                        prob_E = (1 - lambda_) / len(vocab)
                    else:
                        prob_E = lambda_ * emit_dict[next_word] \
                                 + (1 - lambda_) / len(vocab)
                    tmp_score = best_score[i_prev] \
                                 + -math.log(trans_dict[prev_next]) \
                                 + -math.log(prob_E)
                    i_next = '%s %s' % (i + 1, next_tag)
                    if i_next not in best_score or best_score[i_next] > tmp_score:
                        best_score[i_next] = tmp_score
                        best_edge[i_next]  = i_prev
                        #print i_next, next_word ,best_score[i_next]

        # treating the end of sentence #チュートリアル通り
        for prev_tag in tag_dict.keys():
            len_prev = '%s %s' % (len(words), prev_tag)
            prev_eos = '%s </s>' % (prev_tag)
            if len_prev in best_score and prev_eos in trans_dict:
                tmp_score = best_score[len_prev] + -math.log(trans_dict[prev_eos])
                len_eos   = '%s </s>' % (len(words) + 1)
                if len_eos not in best_score or best_score[len_eos] > tmp_score:
                    best_score[len_eos] = tmp_score
                    best_edge[len_eos]  = len_prev
    return best_edge

def backward_step(best_edge, words):
    tags = []
    next_edge = best_edge['%s </s>' % (len(words)+1)]
    while next_edge != '0 <s>':
        position, tag = next_edge.split()
        tags.append(tag)
        next_edge = best_edge[next_edge]
    tags.reverse()
    return tags

def test_hmm(model_file, test_file, result_file):
    r_file = open(result_file, "w")
    import_model(model_file)
    for line in open(test_file):
        words      = line.strip().split()
        best_score = { "0 <s>": 0 }
        best_edge  = { "0 <s>": "NULL" }
        best_edge  = forward_step(best_score, best_edge, words)
        tags_list  = backward_step(best_edge, words)
        r_file.write(' '.join(tags_list) + '\n')
        #print ' '.join(tags_list)


if __name__ == '__main__':
    trans_dict = defaultdict(lambda:.0)
    emit_dict  = defaultdict(lambda:.0)
    tag_dict   = defaultdict(lambda:0)
    vocab      = defaultdict(lambda:0)
    lambda_ = .95

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', dest='model', default="../output/train05_hmm.model", help='writeing model file')
    parser.add_argument('-t', '--test', dest='test', default="../data/wiki-en-test.norm", help='input test data')
    parser.add_argument('-s', '--result', dest='result', default="../output/train05_2.result", help='writeing result file')
    args = parser.parse_args()
    test_hmm(args.model, args.test, args.result)