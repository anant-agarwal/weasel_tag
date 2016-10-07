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
trans_counts = hmm.transition_counts(read["bio_list"],3);
hmm.display_table(trans_counts["counts_table"]);
