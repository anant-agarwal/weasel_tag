# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 11:36:07 2016

"""

import file_reader        
        
def generate_baseline_files(input_folder_path,
                            output_folder_path,
                            baseline_dict) :
    all_text_files = [];
    all_text_files += file_reader.list_all_text_files(input_folder_path);
    
    for file in all_text_files:
        newline = ""
        prev_token = 'O'
        read_handle = open(input_folder_path+file,"r")
        for line in read_handle:
            if not line.strip():
                newline += "\n"
                prev_token = "O"
                continue;
            line_split = line.split();    
            if line_split[0] not in baseline_dict:
                newline += line_split[0]+"\t"+line_split[1]+"\t"+'O'+"\n"
                prev_token = 'O'
            else:
                if prev_token == 'B' or prev_token == 'I' :
                    newline += line_split[0]+"\t"+line_split[1]+"\t"+'I'+"\n"
                    prev_token = 'I'
                else :
                    newline += line_split[0]+"\t"+line_split[1]+"\t"+'B'+"\n"
                    prev_token = 'B'
        write_handle = open(output_folder_path+file,"w");
        write_handle.write(newline)
        write_handle.close();

def generate_weasel_dictionary(folder_path) :
    weasel_dict = dict()    
    all_text_files = [];
    all_text_files += file_reader.list_all_text_files(folder_path);
    
    for file in all_text_files:
        read_handle = open(folder_path+file,"r")
        for line in read_handle:
            if not line.strip():
                continue
            line_split = line.split();
            if (line_split[2] == 'B' or line_split[2] == 'I'):
                #
                # Should we cross check with default weasel words before 
                # marking something as B? can we mark them I directly?
                # 
                weasel_dict[line_split[0]] = line_split[2]
    return weasel_dict
           
           
           
           
           