# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 00:33:48 2016

@author: anant
"""
import file_reader;

def read_everything(folder_path):
# read everything from the train files
# store as list of dictionaryies, reasoning:
#   1) all the 3 columns can be split and processed easily without multiple file i/o
#   2) info of all 3 columns can be used together i.e. reading like a row.
# newline has been entered as \n for all 3 columns -> this is done to make sentence end dectection easy when processing just one column at a time.
    train_corpus = [];
    all_text_files = file_reader.list_all_text_files(folder_path);

    for file in all_text_files:
        read_handle = open(folder_path+file,"r")
        for line in read_handle:
            if not line.strip():
                #if a new line detected
                word = pos = bio = "\n"
            else:
                line_split = line.split()
                word = line_split[0]
                pos = line_split[1]
                bio = line_split[2]
            train_corpus += [{"word":word, "pos":pos, "bio":bio}]

    word_list = [ x["word"] for x in train_corpus ];
    pos_list  = [ x["pos"]  for x in train_corpus ];
    bio_list  = [ x["bio"]  for x in train_corpus ];

    return({
            "word_list":word_list,
            "pos_list":pos_list,
            "bio_list": bio_list,
            "train_corpus": train_corpus
            })


def gen_start_tag(ngram):
# generate start tag, built for finding P(ti|phi)
# phi is the tag occuring before first tag
# #Design Decision begin
# Insert only one <phi> irrespective of ngram, reasons:
#   1. While tagging we will tag one sentence at a time, inter-sentence context for tag transisition is ignored.
#   2. At the beginning we will look only at P(t|<phi>) irrespective of whether we have trigram or ngram etc.
# #Design Decision end
    start_tag = [];

#    for i in range(ngram-1):        #loop to be removed later
#        start_tag += ["<phi>"];
    start_tag = ["<phi>"];
    return start_tag



def bio_list_insert_start_tag(bio_list, ngram):
# returns tags as a list,
# inserts start tags
    start_tag  = gen_start_tag(ngram);
    all_tokens = [];

    all_tokens += start_tag;

    for token in bio_list:
        if not token.strip():
        # insert start tag on seeing new line
            all_tokens += start_tag;
        else:
            all_tokens += [ token ]
    #all_tokens = all_tokens[:-(ngram-1)];   #remove last  n-1 tokens as they will be just start token introduced by last \n.

    return all_tokens;

def transition_counts( bio_list, ngram = 2 ):
# returns counts_table and total_occ_counts which has sum of counts of each row, which will be used to calculate probability
# ngram is feature is built here so as to be able to extend HMM transition probs to trigram etc.
# #Design Decision begin
# Column of <phi> needs to be removed, reason:
#   1. As we are tagging one sentence at a time, so P(<phi>|t) is irrevelant, and that probability mass should be redistributed to others.
#   2. Only rows with Phi are needed as P(t3|t2t1phi) are the only possible combinations. 
# #Design Decision end

    counts_table = dict();

    start_tag_list = gen_start_tag(ngram);
    start_tag_len = len(start_tag_list);
    start_token = start_tag_list[0];

    bio_list = bio_list_insert_start_tag( bio_list, ngram )

    index_tuple = tuple(bio_list[0:start_tag_len]);

    #remove the starting elements as they have been already taken in index_tuple.
    bio_list = bio_list[start_tag_len:];

    #to count all occurances of an index tuple
    total_occ_of_index_tuple = dict();
    for tag in bio_list:
        if not index_tuple in counts_table:
            #if index_tuple is seen for the first time
            counts_table[index_tuple] = dict();
            total_occ_of_index_tuple[index_tuple] = 0;

        if not tag in counts_table[index_tuple]:
            counts_table[index_tuple][tag] = 0

        counts_table[index_tuple][tag] += 1
        total_occ_of_index_tuple[index_tuple] += 1;
        index_tuple = index_tuple+(tag,);
        if(len(index_tuple)>ngram-1):
            index_tuple = index_tuple[1:];

    #removing column <phi>
    for index_tuple in total_occ_of_index_tuple:
        if( start_token in counts_table[index_tuple]):
            #delete from total count:
            total_occ_of_index_tuple[index_tuple] -= counts_table[index_tuple][start_token]
            #delete from count_table:
            del counts_table[index_tuple][start_token]

    return {"counts_table": counts_table, "total_occ_counts": total_occ_of_index_tuple}

def display_table(table):
# displays a table which is a dict of dict
# i.e. 2 dimensional table, can display tables for trigram etc.

    cols_dict = dict();
    for k in table:
        for v in table[k]:
            cols_dict[v] =1;
    cols = cols_dict.keys();
    number_of_cols = len(cols);
    row_format = "{:15}"* (number_of_cols+1);

    print( row_format.format("", *cols))
    for k in table:
        row_contents = [str(k)];
        for v in cols:
            if v in table[k]:
                row_contents += [ str(table[k][v]) ]
            else:
                row_contents += [ "0" ]

        print(row_format.format(*row_contents));
