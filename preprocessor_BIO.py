# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 11:44:41 2016

"""
import os
import file_reader

def preprocess_train_files(input_folder, output_folder) :
    all_text_files = [];
    all_text_files += file_reader.list_all_text_files(input_folder);    
    for file in all_text_files:
        write_handle = open(output_folder+file, "w");
        read_handle = open(input_folder+file, "r")
        new_line = ""
        prev_tag = "_" 
        for line in read_handle:
            tag = "";
            if not line.strip():
                #
                # Every sentence should be processed independently.
                # Insert new line in corresponding trainBIO file
                prev_tag = "_";
                new_line +="\n"
                continue;
            line_split = line.split();    
            if (line_split[2] == '_'):
                #
                # 3rd column value is '_'. Replace that with 'O' 
                prev_tag = '_';
                tag = 'O';
                #
                # Current value in the 3rd column can be CUE-1 OR CUE-2 or CUE-3 etc
                # 3rd check below is to handle case like,
                # a p CUE1
                # b q CUE1
                # c r CUE2
                #
                # output should be,
                # a p B
                # b q I
                # c r B
                #
            else:
                if (prev_tag == '_' or
                    prev_tag != line_split[2]) :
                    #
                    # 3rd column value is CUE* and it is the first occurrence of
                    # CUE* in the current sequence.
                    #
                    prev_tag = line_split[2]
                    tag = 'B';
                elif (prev_tag == line_split[2]):
                    #
                    # 3rd column value is CUE* and previous value in the 3rd column
                    # was also CUE*
                    #
                    prev_tag = line_split[2]               
                    tag = 'I'
            new_line += line_split[0]+"\t"+line_split[1]+"\t"+tag+"\n";           
        write_handle.write(new_line);
        write_handle.close();

def generate_cross_validation_set(folder_path) :
    all_text_files = [];
    all_text_files += file_reader.list_all_text_files(folder_path+"train_BIO");
    dev_test_len = int(len(all_text_files) * 80/100);
    #
    # Assumigng 80% is dev test and 20% is cross validation set.
    #
    file_reader.create_folder(folder_path+"train_BIO"+"/with_tag")
    file_reader.create_folder(folder_path+"train_BIO"+"/without_tag")

    while dev_test_len < len(all_text_files) :
        file = all_text_files[dev_test_len]
        write_handle_1 = open(folder_path+"train_BIO"+"/with_tag/"+file, "w")
        write_handle_2 = open(folder_path+"train_BIO"+"/without_tag/"+file, "w")
        read_handle  = open(folder_path+"train_BIO/"+file, "r")

        line = read_handle.read();
        write_handle_1.write(line)
        write_handle_2.write(line)

        write_handle_1.close();
        write_handle_2.close();

        os.remove(folder_path+"train_BIO/"+file)
        dev_test_len += 1

