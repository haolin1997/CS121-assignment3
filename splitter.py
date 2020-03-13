import json
import os
import time

def splitter(fileloc, mode):

    """
    Split the full_index file to Split index
    to increase Query performance
    """

    with open (fileloc, 'r') as f:
        
        current_letter = 'a'

        while True:

            line = f.readline()

            if not line: #If reach end of the file, Terminate the loop
                break

            if line[2] != current_letter:
                current_letter = line[2]
                
            if mode == 'biword':
                with open('split_biword_file/split_biword_index_%s.txt'%current_letter, 'a') as split:
                    split.write(line)
            elif mode == 'triword':
                with open("split_triword_file/split_triword_index_%s.txt" %current_letter, 'a+') as split:
                    split.write(line)
            elif mode == 'reg':
                with open('split_index_file/split_index_%s.txt'%current_letter, 'a') as split:
                    split.write(line)
                

if __name__ == "__main__":

    #splitter('full_biword_index.txt', 'biword')
    splitter('full_triword_index.txt', 'triword')
    #splitter('full_index.txt','reg')

    
        