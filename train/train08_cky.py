#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/14 19:42:06 Shin Kanouchi
"""ADJP JJ S    0.0120481927710843
JJ  other   0.0223880597014925"""
import argparse
import math
from collections import defaultdict


def import_model(grammar_file):
    nonterm = []  # (親(pos), 子左(pos), 子右(pos), 確率)
    preterm = defaultdict(list)  # pre[右(word)] = [ (左(pos), 確率) ...]
    for rule in open(grammar_file):
        lhs, rhs, prob = rule.strip().split("\t")
        rhs = rhs.split()
        log_prob = math.log(float(prob), 2)
        if len(rhs) == 1:  # 終端記号
            preterm[rhs[0]].append((lhs, log_prob))
        else:  # 非終端記号
            nonterm.append((lhs, rhs[0], rhs[1], log_prob))
    return preterm, nonterm


def add_preterminal(words, preterm):
    best_score = {}
    for i in range(0, len(words)):
        if words[i] in preterm:
            for lhs, log_prob in preterm[words[i]]:
                best_score["%s %d %d" % (lhs, i, i + 1)] = log_prob
    return best_score


def match_nonterm(words, best_score, nonterm):
    best_edge = {}
    for j in range(2, len(words) + 1):  # スパンの右側
        for i in range(j - 2, -1, -1):  # スパンの左側
            for k in range(i + 1, j):
                for sym, lsym, rsym, log_prob in nonterm:
                    l_i_k = "%s %d %d" % (lsym, i, k)
                    r_k_j = "%s %d %d" % (rsym, k, j)
                    s_i_j = "%s %d %d" % (sym, i, j)
                    if l_i_k in best_score and r_k_j in best_score:
                        my_lp = best_score[l_i_k] + best_score[r_k_j] + log_prob
                        if s_i_j not in best_score or my_lp > best_score[s_i_j]:
                            best_score[s_i_j] = my_lp
                            best_edge[s_i_j] = (l_i_k, r_k_j)
    return best_score, best_edge


def test_cky(train_file, test_file, result_file):
    #subroutine_print
    def s_print(p_edge):
        sym, i, j = p_edge.split()
        s_i_j = "%s %s %s" % (sym, i, j)
        if s_i_j in best_edge:  # 非終端記号
            l_edge = best_edge[p_edge][0]
            r_edge = best_edge[p_edge][1]
            return "(%s %s %s)" % (sym, s_print(l_edge), s_print(r_edge))
        else:  # 終端記号
            return ("(%s %s)" % (sym, words[int(i)]))
    #cky
    preterm, nonterm = import_model(train_file)
    r_file = open(result_file, "w")
    for line in open(test_file):
        words = line.strip().split()
        best_score = add_preterminal(words, preterm)
        best_score, best_edge = match_nonterm(words, best_score, nonterm)
        final_best_edge = s_print("S 0 %d" % (len(words)))
        r_file.write("%s\n" % (final_best_edge))
        print final_best_edge

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train', dest='train', default="../data/wiki-en-test.grammar", help='input training data')
    parser.add_argument('-e', '--test', dest='test', default="../data/wiki-en-short.tok", help='input test data')
    parser.add_argument('-r', '--result', dest='result', default="../output/train08_cky.result", help='writing result file')
    args = parser.parse_args()
    test_cky(args.train, args.test, args.result)
