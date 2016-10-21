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
    print("Precision: ", p, "\n")
    print("Recall: ", r, "\n")
    if(p or r):
        return 2*p*r/(p+r)
    else:
        return 0

def sentence_score( truth, gen_file ):
    truth_handle = open(truth,"r")

    i = 0
    for line in truth_handle:
        if(  i ):
            line_split = line.split(",")
            truth_sentence_nums = line_split[1].strip().split(" ")
        i+=1;

    truth_set = set( truth_sentence_nums )

    gen_file_handle = open(gen_file,"r")
    i = 0
    for line in gen_file_handle:
        if( i ):
            line_split = line.split(",")
            gen_file_sentence_nums = (line_split[1]).strip().split(" ")
        i+=1;

    gen_set = set(gen_file_sentence_nums)

    tp = len(gen_set.intersection(truth_set))
    fp = len(gen_set.difference(truth_set))
    fn = len(truth_set.difference(gen_set))

    score = fscore(tp, fp, fn)
    print( score )
    return(score)

def word_score( truth, gen_file ):
    return( sentence_score( truth, gen_file ) )
