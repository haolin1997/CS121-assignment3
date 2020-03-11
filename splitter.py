import json
import os
import time

def splitter():

    """
    Split the full_index file to Split index
    to increase Query performance
    """

    with open ('full_index.txt', 'r') as f:
        
        current_letter = 'a'

        while True:

            line = f.readline()

            if not line: #If reach end of the file, Terminate the loop
                break

            if line[2] != current_letter:
                track_letter[current_letter] = current_index
                current_letter = line[2]
                

            with open('split_index_%s.txt'%current_letter, 'a') as split:
                
                split.write(line)
                

if __name__ == "__main__":

    splitter()
        