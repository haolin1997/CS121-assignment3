from DataFetcher import DataFetcher as DF
from collections import defaultdict
import json
import numpy as np
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import math
import sys
import os
import time
import hashlib


index_breakpoints = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000]


class Indexer():
    """ class to build the inverted index;
        using fetch_content to fetch words from given url
        store them in a map with docID as key and postiong obejct as values"""
        
    def __init__(self):
        self.map = defaultdict(list)
        self.biword_map = defaultdict(list)
        self.triword_map = defaultdict(list)
        self.map_doc_id = {}
        self.checksum_map = []
        self.duplicate = []
        self.file_index = 0
        
    
    def fetch_content(self, id, json_string):
        """ fetch contents from given json string
            store them in the index map """
        json_object = json.loads(json_string)
        url = json_object['url']
        html = json_object['content']
        df = DF(html)
        words = df.get_words()
        biwords = df.get_biwords()
        triwords = df.get_triwords()
        positions = df.get_position()
        checksum = df.get_checksum()
        # === check duplicate ===
        self.check_duplicate(id, checksum)
        # =======================
        self.map_doc_id[id] = url
        for word, count in words.items():
            posting = Posting(id, word, count, positions[word])
            self.map[word].append(posting)
        for biword,count in biwords.items():
            biword_posting = Posting(id, biword, count, 0)
            self.biword_map[biword].append(biword_posting)
        for triword, count in triwords.items():
            triword_posting = Posting(id, triword, count, 0)
            self.triword_map[triword].append(triword_posting)

        #print (len(biwords))
    
    def save_partial_index(self, sort, sort_biword, sort_triword):
        
        with open("inverted_index_%s.txt" %self.file_index, 'w') as f:
            for key, values in sort:
                key_str = '{"' + key + '":'
                f.write(key_str)
                json.dump([p.get_posting() for p in values], f)
                f.write("}\n")
        # save biword index
        with open("inverted_biword_index_%s.txt" %self.file_index, 'w') as f:
            for key, values in sort_biword:
                key_str = '{"' + key + '":'
                f.write(key_str)
                json.dump([p.get_posting() for p in values], f)
                f.write("}\n")
        
        # save triword index
        with open("inverted_triword_index_%s.txt" %self.file_index, 'w') as f:
            for key, values in sort_triword:
                key_str = '{"' + key + '":'
                f.write(key_str)
                json.dump([p.get_posting() for p in values], f)
                f.write("}\n")

        self.file_index += 1  

    
    def save_doc_id(self):
        save_dict = json.dumps(self.map_doc_id)
        f = open('doc_id.json', 'w')
        f.write(save_dict)
        f.close()
        #with open("doc_id.txt", 'w') as f:
            #f.write(str(self.map_doc_id))

    def save_duplicate_id(self):
        save_dict = json.dumps(self.duplicate)
        f = open('duplicate.json', 'w')
        f.write(save_dict)
        f.close()

    def fetch_one(self, path):
        json_file = open(path).readlines()[0]
        self.fetch_content(46591, json_file)
        for i, j in self.biword_map.items():
            #print(i + ": " + str([x.get_posting() for x in j]))
            #print(json.dumps([p.get_posting() for p in j]))
            pass

    def start_index(self):

        index = 0
        for directory in os.listdir('DEV'):
            if directory != '.DS_Store':
                for filenames in os.listdir('DEV/' + directory):
                    index += 1
                    path = 'DEV/'+ directory + '/' + filenames
                    json_file = open(path).readlines()[0]
                    print(path, index)    
                    self.fetch_content(index, json_file)
                    
                    if index in index_breakpoints or index == 55393:
                        temp = sorted(self.map.items())
                        biword_temp = sorted(self.biword_map.items())
                        triword_temp = sorted(self.triword_map.items())
                        self.save_partial_index(temp, biword_temp,triword_temp)
                        self.map = defaultdict(list)
                        self.biword_map = defaultdict(list)
                        self.triword_map = defaultdict(list)
                  
                    if index == 55393:
                        for i in self.duplicate:
                            del self.map_doc_id[str(i)]
                        self.save_doc_id()
                        self.save_duplicate_id()
                    


    def find_file(self, name):
        index = 0
        for directory in os.listdir('DEV'):
            if directory != '.DS_Store':
                for filenames in os.listdir('DEV/' + directory):
                    index += 1
                    path = 'DEV/'+ directory + '/' + filenames
                    json_file = open(path).readlines()[0]
                    json_object = json.loads(json_file)
                    url = json_object['url']
                    self.map_doc_id[index] = url
                    if url == name:
                        print(index, path)
                    
                    #if index == 55393:
                        #self.save_doc_id()


    def check_duplicate(self, id, checksum):
        """ if the checksum exist then add the doc id to the list
            if not, add this id as key and add checksum value to list[0]
        """
        if checksum not in self.checksum_map:
            self.checksum_map.append(checksum)
        else:
            self.duplicate.append(id)
        

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
        




