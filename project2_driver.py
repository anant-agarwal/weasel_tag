# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 21:46:01 2016

"""

import Preprocess_BIO
import baseline      #for first baseline
import baseline1
import kaggle_op

#
# User should enter the directory path having 'train' folder.
#
input_path_is_correct = 0;
while (not input_path_is_correct) :
    #/Users/Deekshith/Desktop/Cornell/2_NLP/assignment_2/nlp_project2_uncertainty/
    path = input("\n\nInput path to the train folder : "); 
    final_path = path+"train/";
    print("\nwill start reading at:", final_path, "\n");    
    confirm = input("If that's right enter yes else no: "); #"yes"
    if (confirm.lower() =="yes") :
        input_path_is_correct = 1


#
# Create output folders.
# One folder for storing preprocessed files
# Second folder for storing the baseline output of test-public
# Third folder for stroing the baseline output of test-private
#
Preprocess_BIO.create_folder(path+"train_BIO")
Preprocess_BIO.create_folder(path+"test-public-baseline1/")
Preprocess_BIO.create_folder(path+"test-private-baseline1/")

#
# Preporces the train folder and replace CUE* with B or I and _ with O
#
Preprocess_BIO.preprocess_train_files(path+"train/", path+"train_BIO/")


'''                             FIRST BASELINE                              '''
'''
#
# After the preprocessing generate dictionary of possible weasel words
#                               
preprocess_dict = baseline.generate_weasel_dictionary(path+"train_BIO/")

baseline.generate_baseline_files(path+"test-public/",
                                 path+"test-public-baseline1/",
                                 preprocess_dict)

baseline.generate_baseline_files(path+"test-private/",
                                 path+"test-private-baseline1/",
                                 preprocess_dict)
                                 
kaggle_op.gen_kaggle_file(path+"test-public-baseline1/",
                          path+"test-private-baseline1/",
                          path)
'''

'''                            SECOND BASELINE                              '''
                          

preprocess_dict = baseline1.generate_weasel_dictionary(path+"train_BIO/")


baseline1.generate_baseline_files(path+"test-public/",
                                 path+"test-public-baseline1/",
                                 preprocess_dict)

baseline1.generate_baseline_files(path+"test-private/",
                                 path+"test-private-baseline1/",
                                 preprocess_dict)
                                 
kaggle_op.gen_kaggle_file(path+"test-public-baseline1/",
                          path+"test-private-baseline1/",
                          path) 