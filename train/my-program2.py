#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/07 15:10:11 Shin Kanouchi
import sys 

def word_segment():
    sentence = "this is a pen"
    words = sentence.split(" ")

    for word in words:
        print word
    print " ||| ".join(words) 
    return len(words)


def add_and_abs(x, y):
    z = x + y
    if z >= 0:
        return z
    else:
        return z * -1


def open_myfile(my_file):
    for line in my_file:
        line = line.strip()
        if len(line) != 0:
            print line


if __name__ == '__main__':
    print "***word_segment***"
    len_words = word_segment()
    print ""

    print "***add_and_abs***"
    print add_and_abs(-6, len_words)
    print ""

    print "***open_myfile***"
    open_myfile(open(sys.argv[1], "r"))