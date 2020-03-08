from DataFetcher import DataFetcher as DF
from collections import defaultdict
import json
import numpy as np
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import math
import sys
import os


index_breakpoints = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000]


class Indexer():
    """ class to build the inverted index;
        using fetch_content to fetch words from given url
        store them in a map with docID as key and postiong obejct as values"""
        
    def __init__(self):
        self.map = defaultdict(list)
        self.map_doc_id = defaultdict(list)
        self.file_index = 0
    
    def fetch_content(self, index, json_string):
        """ fetch contents from given json string
            store them in the index map """
        json_object = json.loads(json_string)
        url = json_object['url']
        html = json_object['content']
        df = DF(html)
        words = df.get_words()
        positions = df.get_position()
        self.map_doc_id[index] = url
        for word, count in words.items():
            #idf = 1 + math.log(count,10)
            posting = Posting(index, word, count, positions[word])
            
            self.map[word].append(posting)
    
    def save_partial_index(self, sort):

        with open("inverted_index_%s.txt" %self.file_index, 'w') as f:
            for key, values in sort:
                key_str = '{"' + key + '":'
                f.write(key_str)
                json.dump([p.get_posting() for p in values], f)
                f.write("}\n")

        self.file_index += 1
    
    def print_index(self, file, size):

        f = open('M1_Report.txt', 'a+')
        f.write("total_unique_tokens: " + str(len(self.map))+ '\n')
        f.write("total_unique_documents: " + str(size) + '\n')
        f.write("total_disk_size: " + str(sys.getsizeof(self.map)) + '\n')
        for word, posting in self.map.items():
            print(word + str( [p.get_posting() for p in posting]))

        f.close()


    def save_dictionary(self, file1, file2):
        """ save the dictionary on outside file """
        np.save(file1, self.map) 
        np.save(file2, self.map_doc_id)

    def start_index(self):

        '''
        path = '/Users/Frank/Documents/GitHub/CS121-assignment3/DEV/www_ics_uci_edu/7bca1e4120df36bda6087963c3a397d7f80f22b4029a3fa9b09d1930097ce354.json'
        json_file = open(path).readlines()[0]
        self.fetch_content(1, json_file)
  
        if self.file_index in index_breakpoints:
            print(self.map)
            temp = sorted(self.map.items())
            self.save_partial_index(temp)
            self.map = {}
        '''
        
        index = 0
        for directory in os.listdir('DEV'):
            if directory != '.DS_Store':
                for filenames in os.listdir('DEV/' + directory):
                    path = 'DEV/'+ directory + '/' + filenames
                    json_file = open(path).readlines()[0]
                    print(path, index)    
                    self.fetch_content(index, json_file)
                    if index in index_breakpoints or index == 55391:
                        temp = sorted(self.map.items())
                        self.save_partial_index(temp)
                        self.map = defaultdict(list)
                    index += 1
        
        #index.save_dictionary('my_file.npy', 'my_file_doc.npy')
    
        
    



class Posting():
    """ the posting object. 
        arrtibutes: 
            the docID;
            the word this posting object related to; 
            the word counts;
            position of the word in this particular document
    """
    def __init__(self,id, word, word_counts, position):
        self.id = id
        self.word = word
        self.score = word_counts  
        self.position = position

    def get_posting(self):
        """ return the content of the posting object as a list
            [docID, score, position of the word]
        """
        return [self.id, self.score]
        




