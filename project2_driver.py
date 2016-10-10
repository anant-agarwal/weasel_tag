# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 21:46:01 2016

"""

import preprocessor_BIO
import baseline      #for first baseline
import baseline1
import kaggle_op
import file_reader
import hmm
import nltk
import checker

local_run = 1;

if( local_run ):
    import proj_config;
    path = proj_config.path;
    final_path = path+"train/";
    baseline_number =1;
else:

    #
    # User should enter the directory path having 'train' folder.
    #
    input_path_is_correct = 0;
    while (not input_path_is_correct) :
        path = input("\n\nInput path to the train folder : ");
        final_path = path+"train/";
        print("\nwill start reading at:", final_path, "\n");
        confirm = input("If that's right enter yes else no: "); 
        if (confirm.lower() =="yes") :
            input_path_is_correct = 1
        baseline_number = int(input("Enter baseline number:"));    


#
# Create output folders.
# One folder for storing preprocessed files
# Second folder for storing the baseline output of test-public
# Third folder for stroing the baseline output of test-private
#
file_reader.create_folder(path+"train_BIO")
file_reader.create_folder(path+"test-public-baseline1/")
file_reader.create_folder(path+"test-private-baseline1/")
file_reader.create_folder(path+"test-public-hmm/")
file_reader.create_folder(path+"test-private-hmm/")

#
# Preporces the train folder and replace CUE* with B or I and _ with O
#
preprocessor_BIO.preprocess_train_files(path+"train/", path+"train_BIO/")


'''
There are 2 Baselines: {1,2} set baseline_number accordingly to run them

''
#
# After the preprocessing generate dictionary of possible weasel words
#



if(baseline_number == 1):
    run_baseline = baseline;
elif(baseline_number == 2):
    run_baseline = baseline1;
else:
    print("baseline enum is {1,2}\n");
preprocess_dict = run_baseline.generate_weasel_dictionary(path+"train_BIO/")


run_baseline.generate_baseline_files(path+"test-public/",
                                 path+"test-public-baseline1/",
                                 preprocess_dict)

run_baseline.generate_baseline_files(path+"test-private/",
                                 path+"test-private-baseline1/",
                                 preprocess_dict)

kaggle_op.gen_kaggle_file(path+"test-public-baseline1/",
                          path+"test-private-baseline1/",
                          path)
'''

''' sample code for integrating HMM code done till now  is below:'''
read = hmm.read_everything(path+"train_BIO/");
#start_tag = hmm.gen_start_tag(3);
#bio_list = hmm.bio_list_insert_start_tag(read["bio_list"], 2);
trans_counts = hmm.transition_counts(read["bio_list"],2);
trans_probs = hmm.transition_probs(read["bio_list"], 2);
em_counts = hmm.emission_counts(read["train_corpus"]);
em_probs = hmm.emission_probs(read["train_corpus"]);
#hmm.display_table(trans_counts["counts_table"]);
#hmm.display_table(trans_probs);
#hmm.display_table(em_counts["counts_table"]);
#hmm.gen_hmm_tag(path+"train_BIO/", path+"test-public/", path+"test-public-hmm/", 2)
#hmm.gen_hmm_tag(path+"train_BIO/", path+"test-private/", path+"test-private-hmm/", 2)
#kaggle_op.gen_kaggle_file(path+"test-public-hmm/",
#                          path+"test-private-hmm/",
#                          path,
#                          "hmm")
#'''
                          
                          
''' ********* CV Block ************* '''    
preprocessor_BIO.generate_cross_validation_set(path)
                      
hmm.gen_hmm_tag(path+"train_BIO/", path+"cv_test/", path+"cv_test/", 2)
#hmm.gen_hmm_tag(path+"train_BIO/", path+"test-private/", path+"test-private-hmm/", 2)

kaggle_op.gen_kaggle_file(path+"cv_truth/", #public test data 
                          path+"test-private-hmm/",     #private test data
                          path,                     #output path
                          "test_truth",             #file_tag
                          1)                        #only public = ?

kaggle_op.gen_kaggle_file(path+"cv_test/",
                          path+"test-private-hmm/",
                          path,
                          "test_gen",1)

                          
checker.sentence_score(path+"_test_truth_kag_sent_op.csv",path+"_test_gen_kag_sent_op.csv" )
checker.sentence_score(path+"_test_truth_kag_word_op.csv",path+"_test_gen_kag_word_op.csv" )
''''''