# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 16:58:36 2016

@author: anant

code checker
"""
def precision(tp, fp):
    return tp/(tp+fp)

def recall(tp, fn):
    return tp/(tp+fn)

def fscore( tp, fp, fn):
    p = precision(tp, fp)
    r = recall(tp, fn)
    return 2*p*r/(p+r)

def sentence_score( truth, gen_file ):
    truth_handle = open(truth,"r")

    i = 0
    for line in truth_handle:
        if( not i ):
            continue
        line_split = line.split(",")
        truth_sentence_nums = line_split[1].split(" ")

    truth_set = set( truth_sentence_nums )

    gen_file_handle = open(truth,"r")
    i = 0
    for line in gen_file_handle:
        if( not i ):
            continue
        line_split = line.split(",")
        gen_file_sentence_nums = line_split[1].split(" ")

    gen_set = set(gen_file_sentence_nums)

    tp = len(gen_set.intersection(truth_set))
    fp = len(gen_set.difference(truth_set))
    fn = len(truth_set.difference(gen_set))

    score = fscore(tp, fp, fn)
    print( score )
    return(score)

def word_score( truth, gen_file ):
    return( sentence_score( truth, gen_file ) )
