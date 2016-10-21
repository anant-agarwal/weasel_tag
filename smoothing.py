# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 14:31:09 2016

@author: Deekshith
"""
import nltk

def interpolate_get_freq(freq_of_freq, non_zero_arr, index):
    value = 0;
    index = int(index)
    if(non_zero_arr[index] != index ):
        value = freq_of_freq[non_zero_arr[index]]/(non_zero_arr[index]-index+1);
    else:
        value = freq_of_freq[index];
    return value;

def add_uknown_word_corpus(word_list) :
    word_list.append('<unk>')
    return word_list;

#
''' TODO : Anant, please look at the interpolation code, i have added a hack! '''

#
# Move this to a new file once we have this working!!
# add a column for unknown/unseen words for B I O
#
def good_turing_smoothing(em, word_list) :

    word_list_dict = dict()
    word_list_dict = nltk.FreqDist(word_list)

    #
    ''' Find out the max_freq value '''
    #
    max_freq = len(word_list_dict.keys()) * 3;
    freq_of_freq = [];

    i = 0;
    while i <= max_freq :
        freq_of_freq.append(0); #Instead try with arrays.
        i += 1;

    counts_table = em["counts_table"]
    total_counts = em["total_occ_counts"]

    max_freq = -1;
    #
    # For each unique word in the corpus
    #   for each tag in [B, I, O]
    #       check if we have a column entry for the chosen word for the chosen key
    #       if column is not found, then it is a unknown/unseen word, account that
    #       bigram as bigram apperaring with the frequency of zero.
    #       else if we find the entry in the column, update freq_of_freq table
    #       Keep track of bigram with maximum frequency, do not consider bigrams appearing 0 times.
    #
    for key in word_list_dict:
        for tag in ['B', 'I', 'O']:
            try :
                frequency = int(counts_table[tag][key])
            except :
                frequency = 0;
            try :
                freq_of_freq[frequency] += 1;
            except:
                # not good for us, have to tune 40000 value above
                print("Out of bound! ",frequency, key, tag)
            if freq_of_freq[frequency] > max_freq and frequency != 0:
                max_freq = freq_of_freq[frequency]

        '''           GOOD TRUING SMOOTHING (EDIT COMMENTS HERE )            '''
    #
    # C* = (c+1)*Nc+1/Nc (what if Nc is zero)
    #
    # Applicable only for frequencies whihc are less than k(=5 for now)
    # We are going to do smothing only for bigrams.
    # in case of unigram N0 and N1 will be zero!
    #

    non_zero_index_arr = [];
    freq_of_freq_index = 0;
    next_non_zero_index = 0;
    for v in freq_of_freq:
        if(v != 0):
            next_non_zero_index = freq_of_freq_index;
        elif(next_non_zero_index < freq_of_freq_index):
            next_non_zero_index = freq_of_freq_index;
            while(freq_of_freq[next_non_zero_index] == 0):
                next_non_zero_index += 1;
                '''    HACK '''
                if (next_non_zero_index >= 7000):
                    break;
        non_zero_index_arr.append(next_non_zero_index);
        freq_of_freq_index += 1;
    k = 5; ##### parameter to be tuned with dev set

    for key in word_list_dict:
        for tag in ['B', 'I', 'O']:
            try :
                c = counts_table[tag][key]
            except :
                c = 0
            if (c < k):
                new_c = ((c+1)*
                         (interpolate_get_freq(freq_of_freq, non_zero_index_arr,c+1)/
                          interpolate_get_freq(freq_of_freq, non_zero_index_arr, c)));
                #
                # Tag vs word table already had a column for word for the chosen tag
                # Replace the current value c with new value c*
                #
                if key in counts_table[tag]:
                    counts_table[tag][key] += new_c
                    counts_table[tag][key] -= c
                    total_counts[tag] += new_c
                    total_counts[tag] -= c
                    #print("value changed from",c,"to ",new_c)
                else:
                    #
                    # unseen word,tag combination in corpus
                    #
                    assert(c == 0)
                    counts_table[tag]['<zero>'] = new_c
                    total_counts[tag] += new_c

    return {"counts_table": counts_table, "total_occ_counts": total_counts}
