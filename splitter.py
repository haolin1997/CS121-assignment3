import json
import os
import time

if __name__ == "__main__":

    with open ('full_index.txt', 'r') as f:
        
        current_letter = 'a'
        current_index = 0
        current_file_index = 0

        track_letter = {}

        while True:

            line = f.readline()
            if not line:
                break

            if line[2] != current_letter:
                track_letter[current_letter] = current_index
                current_letter = line[2]
                

            with open('split_index_%s.txt'%current_letter, 'a') as split:
                
                split.write(line)
                current_index += 1

        with open('track_letter.txt', 'a') as track:
            json.dump(track_letter, track)
        