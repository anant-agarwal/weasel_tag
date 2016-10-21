# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 00:33:48 2016

@author: anant
"""
import file_reader
import smoothing
import nltk

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

def transition_counts( bio_list, ngram ):
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

    bio_list = bio_list_insert_start_tag(bio_list, ngram)

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
    '''original_o =  counts_table[('O',)]['O'];
    counts_table[('O',)]['O']  = 3* counts_table[('O',)]['B'] #/=20;
    total_occ_of_index_tuple[('O',)] -= (original_o -     counts_table[('O',)]['O']);'''
    return {"counts_table": counts_table, "total_occ_counts": total_occ_of_index_tuple}


def transition_probs( bio_list, ngram =2 ):
#returns transition probabilities
# #TODO: Think about smoothing.
    trans = transition_counts(bio_list, ngram)
    counts_table = trans["counts_table"]
    total_counts = trans["total_occ_counts"]
    trans_prob = counts_table;
    for index_tuple in total_counts:
        for cell in counts_table[index_tuple]:
            trans_prob[index_tuple][cell] /= total_counts[index_tuple]
    return(trans_prob)

def add_uknown_word_corpus(word_list) :
    word_list.append('<unk>')
    return word_list;

def emission_counts( train_corpus):
#returns count of words per tag and total occurence of a tag, to be used for calculating P(w|t)
    counts_table = dict()
    total_occ = dict();

    for line in train_corpus:
        word = line["word"];
        if( word == "\n"):
            continue
        #pos = line["pos"];
        bio = line["bio"];
        if not bio in counts_table:
            counts_table[bio] = dict()
            total_occ[bio] = 0
        if( not word in counts_table[bio] ):
            counts_table[bio][word]=0;
        '''
        # Handling unseen words using pos tags
        if( not pos in counts_table[bio] ):
            counts_table[bio][pos] = 0;
        counts_table[bio][pos] +=  1;
        counts_table[bio][word] += 1;
        total_occ[bio] += 2
        continue;
        '''

        counts_table[bio][word] +=1;
        total_occ[bio] += 1;
    #
    # Unknown word handing. Add a column '<unk>' for each tag and update the
    # table[tag]['<unk>'] with the ratio of tag count/summation of all the tag
    # counts
    #
    total_bio_count = total_occ['B'] + total_occ['I'] + total_occ['O']

    for bio in ['B', 'I', 'O']:
        word = '<unk>'
        if( not word in counts_table[bio] ):
            #counts_table[bio][word] = 0
            counts_table[bio][word] = (total_occ[bio]/total_bio_count)
            total_occ[bio] += (total_occ[bio]/total_bio_count)
    return {"counts_table": counts_table, "total_occ_counts": total_occ}

def emission_probs( train_corpus, word_list ):
#returns emmision probabilities
# #TODO: Think about smoothing
    em = emission_counts(train_corpus)
    word_list = add_uknown_word_corpus(word_list)
    em = smoothing.good_turing_smoothing(em, word_list)
    counts_table = em["counts_table"]
    total_counts = em["total_occ_counts"]
    em_prob = counts_table;
    for bio in total_counts:
        for cell in counts_table[bio]:
            em_prob[bio][cell] /= total_counts[bio]
    return(em_prob)

def tag_new_sentence( sentence, em_probs, trans_probs, ngram ):
    sentence = [{"word": "<phi>", "em":{"B":1,"I":1,"O":1}, "bp":{}, "pos": "<phi>"}] + sentence
    sent_len = len( sentence )
    handle_unseen_with_pos = 0

    for i in range(1, sent_len):
        curr_column = sentence[i]
        prev_column = sentence[i-1]
        curr_column["em"] = dict();
        curr_column["bp"] = dict();
        for tag in ['B', 'I', 'O']:
            #
            # For each tag, see if word is present in column
            # if not word can be uknown or unseen
            #
            if curr_column["word"] in em_probs[tag] :
                em_prob = em_probs[tag][curr_column["word"]]
            elif handle_unseen_with_pos :
                try :
                    em_prob = em_probs[tag][curr_column["pos"]]
                except :
                    em_prob = 0.0000000001
            else :
                #
                # unseen or unknown word
                #
                #em_prob = 0.00001
                if (curr_column["word"] in em_probs['B'] or
                    curr_column["word"] in em_probs['I'] or
                    curr_column["word"] in em_probs['O']) :
                        #
                        # word, tag comination is unseen in corpus
                        #
                        em_prob = em_probs[tag]['<zero>']
                else :
                        em_prob = em_probs[tag]['<unk>']
            maxi = -1;
            bp_tag = "";
            for prev_tag in ['B', 'I', 'O']:
                try:
                    trans_prob = trans_probs[(prev_tag,)][tag];
                except:
                    #display_table(trans_probs);
                #    print(prev_tag, tag)
                    trans_prob = 0;
                state_trans_prob = trans_prob * prev_column["em"][prev_tag]
                if( maxi < state_trans_prob ):
                    maxi = state_trans_prob
                    bp_tag = prev_tag

            curr_state_prob = maxi * em_prob
            curr_column["em"][tag] = curr_state_prob
            curr_column["bp"][tag] = bp_tag

        sentence[i] = curr_column

    #check which one is max for last word
    maxi = -1;
    max_tag = "";
    for tag in ['B','I','O']:
        if( maxi < sentence[-1]["em"][tag]):
            maxi = sentence[-1]["em"][tag]
            max_tag = tag

    sentence[-1]["bio"] = max_tag

    #backtrace now:
    j = sent_len -2;
    while(j>0):
        sentence[j]["bio"]= sentence[j+1]["bp"][sentence[j+1]["bio"]]
        j -=1

    #remove entry for <phi> and return
    return (sentence[1:])

def gen_hmm_tag( train_folder_path, test_folder_path, output_folder_path, ngram = 2, config = {}):
#this is the driver function for this file
#it reads all the test data, puts it in appropriate data structures and initiates tagging.
#We are tagging one sentence at a time.
#parameter config is a dictionary, for controlling the type of tagging:
#   Insert a key w_and_pos to change emission probs to P(w.pos | t)
#   Insert a key pos_only to change emission probs to P( pos | t)
#   Insert a key prune_train with tupel (B,I,O) to preune the training data
    training_data = read_everything( train_folder_path )
    if( "prune_train" in config ):
        if( type(config["prune_train"]) != type( () ) or len(config["prune_train"]) != 3 ):
            print("****ERROR: prune_train should be a 3tuple")
        prune_config = config["prune_train"]
        training_data = prune_train_data( training_data, prune_config[0], prune_config[1], prune_config[2] )

    if( "w_and_pos" in config ):
        training_data = word_pos(training_data)
    if( "pos_only" in config ):
        training_data = pos_instead_of_word(training_data)

    em_probs = emission_probs(training_data["train_corpus"] , training_data["word_list"] )
    trans_probs = transition_probs(training_data["bio_list"], ngram )
    all_text_files = file_reader.list_all_text_files(test_folder_path)
    for file in all_text_files:
        read_handle = open(test_folder_path+file,"r")
        sentence = [];
        tagged_words_list = []
        #original_text = read_handle.read();

        for line in read_handle:
            #print(line)
            if(not line.strip()): #=="\n"
                    #one sentence has been read, intitiate tagging:
                    if("w_and_pos" in config):
                        sentence = word_pos_test_sent(sentence)
                    if("pos_only" in config ):
                        sentence = pos_instead_of_word_test_sent(sentence)

                    tagged_sentence = tag_new_sentence( sentence, em_probs, trans_probs, ngram )
                    tagged_words_list += unroll_dict( tagged_sentence, config )
                    tagged_words_list[-1] += "\n" #this is to add an empty new line after sentence
                    #reset sentence[] to process new sentence
                    #unknown_word_count += tag_op[2]
                    #unseen_word_count += tag_op[1]
                    sentence = []
            else:
                line_split = line.split()
                word = line_split[0]
                pos = line_split[1]
                sentence += [{"word":word, "pos":pos}]
        new_file_content = "\n".join(tagged_words_list)
        read_handle = open(test_folder_path+file,"r")
        original_text = read_handle.read()
        if(len(new_file_content) + 1 != len(original_text)):
            print(new_file_content)
        
        write_handle = open(output_folder_path+file,"w");
        write_handle.write(new_file_content)
        write_handle.close();

def unroll_dict( dict_list, config = {}):
# dict_list is a list of dictionaries.
# each element of dict_list is converted into a string and added to list.
# A list of the form: [...,"abc POS B",... ]    is returned
    arr = [];
    for k in dict_list:
        word = k["word"]
        pos = k["pos"]
        bio = k["bio"]

        if( "w_and_pos" in config ):
            word = word[0]
        elif("pos_only" in config):
            temp = word
            word = pos
            pos = temp

        arr += [word+"\t"+pos+"\t"+bio];
    return arr


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
                row_contents += [ str(table[k][v])[0:10] ]
            else:
                row_contents += [ "0" ]

        print(row_format.format(*row_contents));

def word_pos ( training_data ):
# modifies training data so that word is (word,pos) and all the rest of the code works out of the box for it.
    corpus = training_data["train_corpus"]
    i = 0;
    word_list = []
    for element in corpus:
        tup = (corpus[i]["word"], corpus[i]["pos"]);
        corpus[i]["word"] = tup
        word_list += [tup]
        i += 1
    training_data["train_corpus"] = corpus
    training_data["word_list"] = word_list
    return training_data

def word_pos_test_sent( sentence ):
#This is similar to function word_pos, just that it is transforming the test sentence so that P(word.pos | t) works
    new_sent = sentence;
    i = 0;
    for element in sentence:
        new_sent[i]["word"] = (element["word"], element["pos"])
        i += 1
    return(new_sent)


def pos_instead_of_word (training_data):
# modifies training data so that word is replaced by pos and all the rest of the code works out of the box for it.
    corpus = training_data["train_corpus"]
    i = 0;
    for element in corpus:
        corpus[i]["word"] = element["pos"]
        corpus[i]["pos"] = element["word"]
        i += 1

    training_data["train_corpus"] = corpus
    training_data["word_list"] = training_data["pos_list"]
    return training_data

def pos_instead_of_word_test_sent( sentence ):
#This is similar to function pos_instead_of_word, just that it is transforming the test sentence so that P(pos | t) works
    new_sent = sentence;
    i = 0;
    for element in sentence:
        new_sent[i]["word"] = element["pos"]
        new_sent[i]["pos"] = element["word"]
        i += 1
    return(new_sent)

def prune_train_data( training_data, b_up, i_up, o_down ):
# after seeing o_down number of Os drop the next O which occurs immediately after,
# we only want to prune oooo to a smaller length, and not things like oooboo as we dont wanna loose the
# transition probability of OB or IO
# for b_up (i_up), just insert a b-word(i-word) after seeing b_up(i_up) number of Bs (Is)
# pass -1 for any of b_up,  i_up, o_down if you dont want them to be affected.
    bio_list  = training_data["bio_list"]
    corpus = training_data["train_corpus"]
    new_corpus = []
    i = 0
    prev = ""
    o_counts = 0
    b_counts = 0
    i_counts = 0
    for element in corpus:
        new_corpus += [element]
        if( bio_list[i] == "B" ):
            b_counts += 1
            if(b_counts == b_up):
                    new_corpus += element
                    b_counts = 0
        if( bio_list[i] == "I" ):
            i_counts += 1
            if(i_counts == i_up):
                    new_corpus += element
                    i_counts = 0

        if( bio_list[i]== "O"):
            if( prev != 'O'):
                o_counts = 0
            o_counts +=1
            if(o_counts == o_down + 1):
                del( new_corpus [-1] )
                o_counts =0
        prev = bio_list[i]
        i +=1

    word_list = [ x["word"] for x in new_corpus ];
    pos_list  = [ x["pos"]  for x in new_corpus ];
    bio_list  = [ x["bio"]  for x in new_corpus ];

    return({
            "word_list":word_list,
            "pos_list":pos_list,
            "bio_list": bio_list,
            "train_corpus": new_corpus
            })
