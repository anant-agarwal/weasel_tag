"""
Created on Sat Oct  1 15:20:14 2016

"""
import file_reader

#op_path = proj_config.baseline1_public_path;

def gen_kaggle_op_lists(op_path):
   all_text_files = file_reader.list_all_text_files(op_path);
   word_counter = 0;
   sentence_counter = 0;
   sentence_output = [];
   
   amb_words_per_sent_count = 0;
   
   output = [];
   output_len = 0;
   prev_tag = ""
   #below line for testing with one file.
   #all_text_files = ["doc_0501.txt"]; #all_text_files[0]
   for file in all_text_files:
       read_handle = open(op_path+file,"r");    
          
       for line in read_handle:
           if not line.strip():
               #
               # Chnage the equation to > 2 if first baseline approach is 
               # chosen.
               #
               if(amb_words_per_sent_count > 0):
                   sentence_output += [str(sentence_counter)," "];
               amb_words_per_sent_count = 0;    
               sentence_counter += 1;    
               continue;    
               
           line_split = line.split();  
           if(('B' == line_split[2] and prev_tag != 'O' and prev_tag!="") 
           or ('O' == line_split[2] and prev_tag != 'O' and prev_tag !="")) :
               output += ["-",str(word_counter-1)];
               output_len += 2;
   
           if('I' == line_split[2]):
               if (prev_tag == 'B') :
                   amb_words_per_sent_count += 1;
   
           if('B' == line_split[2] or ('I' == line_split[2] and prev_tag == 'O')) :
               output += [" ",str(word_counter)];#this will add an extra space in the begining.
               output_len += 2;
               amb_words_per_sent_count += 1; #(count only sequence of Is as 1 for now)
           word_counter += 1;
           prev_tag = line_split[2]

   print("Total number of words in", op_path," : ", word_counter-1, "\n");
   print("Total number of sentences in", op_path, ": ", sentence_counter-1, "\n");
   return([output, sentence_output]);

def gen_kaggle_file(public_path, private_path, file_write_path):
   word_file_content = "Type,Spans\n";
   sent_file_content = "Type,Indices\n";
   
   public_output = gen_kaggle_op_lists(public_path);
   private_output = gen_kaggle_op_lists(private_path);
   word_file_content += "CUE-public,"+"".join(public_output[0][1:])+"\n";
   word_file_content += "CUE-private,"+"".join(private_output[0][1:])+"\n";
       
   sent_file_content += "SENTENCE-public," + "".join(public_output[1])+"\n";
   sent_file_content += "SENTENCE-private," + "".join(private_output[1])+"\n";
   
   write_word_handle = open(file_write_path+"kag_word_op.csv", "w");
   write_word_handle.write(word_file_content);
   
   write_sent_handle = open(file_write_path+"kag_sent_op.csv", "w");
   write_sent_handle.write(sent_file_content);