# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 13:43:30 2016

@author: anant

Read all files 

"""
import os;

def read_file( path_to_file ):
    file_handle = open( path_to_file,"r");
    return file_handle.read();

def list_all_text_files( path ):
    all_files = os.listdir(path);
    all_text_files = [];
    for file_name in all_files:
        if( file_name.endswith(".txt") ):
            all_text_files.append(file_name);
    return(all_text_files);
        
def read_lines_as_list(path_to_file):
    with open(path_to_file) as f:
        line_list = f.readlines();     
    return(line_list);
    