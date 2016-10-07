# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 11:44:41 2016

"""
import file_reader
import os
import shutil


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)
  
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

