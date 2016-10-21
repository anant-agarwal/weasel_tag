# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 23:31:51 2016

@author: Deekshith
"""

import file_reader
import os

def compare_results(folder_path):
    cv_test = folder_path+"cv_test/"
    cv_truth = folder_path+"cv_truth/";
    all_text_files = []
    all_text_files += file_reader.list_all_text_files(cv_test);

    compare_truth_test = folder_path+"compare_truth_test/"
    file_reader.create_folder(compare_truth_test)

    correct_prediction = 0;
    incorrect_prediction = 0;
    total_prediction = 0;
    count_B = 0
    count_I = 0
    count_O = 0

    write_handle_all_files = open(folder_path+"all_files.txt", "w")
    all_files_compare_data = ""

    for file in all_text_files:
        new_line = ""
        read_handle_truth = open(cv_truth+file, "r")
        read_handle_test  = open(cv_test+file, "r")
        write_handle_compare = open(compare_truth_test+file, "w")

        for line1, line2 in zip (read_handle_truth, read_handle_test) :
            if not line1.strip():
                assert (not line2.strip())
                write_handle_compare.write(line1)
                continue;
            line1_split = line1.split()
            line2_split = line2.split()
            if (line1_split[2] == line2_split[2]) :
                matching = ""
                correct_prediction += 1;
            else:
                matching = "NO"
                all_files_compare_data += line1_split[0].rjust(15)+line1_split[1].rjust(5)+line1_split[2].rjust(5)+line2_split[2].rjust(5)+matching.rjust(5)+"\n";
                incorrect_prediction += 1
            total_prediction += 1
            '''
            assert (len(line1_split[0]) == len(line2_split[0]) and
                    len(line1_split[1]) == len(line2_split[1]))
                    '''
            if (line1_split[2] == 'O'):
                count_O += 1
            elif (line1_split[2] == 'B'):
                count_B += 1
            else:
                count_I += 1
            new_line += line1_split[0].rjust(15)+line1_split[1].rjust(5)+line1_split[2].rjust(5)+line2_split[2].rjust(5)+matching.rjust(5)+"\n";
        write_handle_compare.write(new_line);
        write_handle_compare.close();
    write_handle_all_files.write(all_files_compare_data)
    write_handle_all_files.close()
    #print("\nIncorrect prediction =",incorrect_prediction)
    #print("Correct prediction =",correct_prediction)
    #print("Total prediction =",total_prediction)
    #print("Incorrect prediction ratio", incorrect_prediction/total_prediction)
    #print("\nCount of B =",count_B)
    #print("Count of I = ",count_I)
    #print("Count of O =",count_O)

def generate_cross_validation_set(folder_path) :
    all_text_files = [];
    all_text_files += file_reader.list_all_text_files(folder_path+"train_BIO");
    dev_test_len = int(len(all_text_files) * 80/100);
    #
    # Assumigng 80% is dev test and 20% is cross validation set.
    #
    cv_truth = folder_path+"cv_truth/";
    cv_test = folder_path+"cv_test/"

    file_reader.create_folder(cv_truth)
    file_reader.create_folder(cv_test)

    while dev_test_len < len(all_text_files) :
        file = all_text_files[dev_test_len]
        write_handle_1 = open(cv_truth+file, "w")
        write_handle_2 = open(cv_test+file, "w")
        read_handle  = open(folder_path+"train_BIO/"+file, "r")

        line = read_handle.read();
        write_handle_1.write(line)
        write_handle_2.write(line)

        write_handle_1.close();
        write_handle_2.close();

        os.remove(folder_path+"train_BIO/"+file)
        dev_test_len += 1
