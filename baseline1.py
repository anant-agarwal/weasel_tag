# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 00:32:05 2016


"""

import random;
import file_reader

baseline_dict = dict()

def generate_weasel_dictionary(folder_path):
    all_text_files = [];
    all_text_files += file_reader.list_all_text_files(folder_path);
    for file in all_text_files:
        read_handle = open(folder_path+file,"r")
        for line in read_handle:
            if not line.strip():
                continue
            line_split = line.split()
            if(not line_split[0] in baseline_dict):
                baseline_dict[line_split[0]] = {"B": 0, "I": 0, "O": 0};
                baseline_dict[line_split[0]][line_split[2]] += 1;                                 
    return baseline_dict

def generate_baseline_files(folder_path, output_folder_path,baseline_dict) :
    all_text_files = [];
    all_text_files += file_reader.list_all_text_files(folder_path);
    for file in all_text_files:
        newline = ""
        read_handle = open(folder_path+file,"r")
        for line in read_handle:
            if not line.strip():
                newline += "\n"
                continue;
            line_split = line.split();    
            if line_split[0] not in baseline_dict:
                newline += line_split[0]+"\t"+line_split[1]+"\t"+'O'+"\n"
            else:
                word_tag_count = baseline_dict[ line_split[0]];
                word_tag_cumm = [ word_tag_count["B"],word_tag_count["B"]+word_tag_count["I"], word_tag_count["B"]+word_tag_count["I"]+word_tag_count["O"]];
                total = word_tag_cumm[-1];
                word_tag_prob = [ word_tag_cumm[0]/total, word_tag_cumm[1]/total, word_tag_cumm[2]/total];                  
                random_num = random.random();
                if(random_num < word_tag_prob[0]):
                    tag = "B"
                elif(random_num < word_tag_prob[1]):
                    tag ="I"
                elif(random_num<word_tag_prob[2]):
                    tag = "O";
                else:
                    print("wrong");
                newline += line_split[0]+"\t"+line_split[1]+"\t"+tag+"\n"
        write_handle = open(output_folder_path+file,"w");
        write_handle.write(newline)
        write_handle.close();