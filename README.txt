


How to run the code :
=====================

— Run assignment2_driver.py [We have used ‘Anaconda’ with ’Spyder’ IDE for the development (python 3.5)]
- User should enter the folder path which contains the folder ’train’. 

- Output will be stored in the folder path passed above by the user. We also create 3 folders to store the preprocessed files and baseline files.


Console Output :
================

Input path to the train folder : /Users/Deekshith/Desktop/Cornell/2_NLP/assignment_2/nlp_project2_uncertainty/

will start reading at: /Users/Deekshith/Desktop/Cornell/2_NLP/assignment_2/nlp_project2_uncertainty/train/ 

If that's right enter yes else no: yes
Total number of words in /Users/Deekshith/Desktop/Cornell/2_NLP/assignment_2/nlp_project2_uncertainty/test-public-baseline1/  :  55758 

Total number of sentences in /Users/Deekshith/Desktop/Cornell/2_NLP/assignment_2/nlp_project2_uncertainty/test-public-baseline1/ :  2006 

Total number of words in /Users/Deekshith/Desktop/Cornell/2_NLP/assignment_2/nlp_project2_uncertainty/test-private-baseline1/  :  55663 

Total number of sentences in /Users/Deekshith/Desktop/Cornell/2_NLP/assignment_2/nlp_project2_uncertainty/test-private-baseline1/ :  2003 

>>> 

Code Organization :
===================

We have created following modules to do required tasks in this project.

1) assignment2_driver.py
	Driver for the entire project. Imports other modules to do required tasks.
	Interacts with User and requests for input. Also creates 3 directories to save the output of preprocess and baseline of test-public and test-private folder.

2) file_reader.py
	Folder path is passed and reads all the file names and stores them in a list.

3) Preprocess_BIO.py
	Replaces instance of CUE* in train folder to sequence of B, I and O.
	
4) baseline1.py and baseline.py
	Generates a weasel dictionary and output baseline files. We have two baseline files and at a time one of the baseline can be chosen to perform the sequence tagging task.

5) kaggle_op.py
	Generates the gaggle output based on the baseline files generated for test-public and test-private folders.
