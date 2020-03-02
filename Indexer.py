
import DataFetcher as DF
from collections import defaultdict
import json
import numpy as np


class Indexer():
    """ class to build the inverted index;
        using fetch_content to fetch words from given url
        store them in a map with docID as key and postiong obejct as values"""
        
    def __init__(self):
        self.map = defaultdict(list)
        self.map_doc_id = defaultdict(list)
    
    def fetch_content(self, index, json_string):
        """ fetch contents from given json string
            store them in the index map """
        json_object = json.loads(json_string)
        #json_object = json_string 
        url = json_object['url']
        html = json_object['content']
        df = DF(html)
        words = df.get_words()
        positions = df.get_position()
        self.map_doc_id[index] = url
        for word, count in words.items():
            posting = Posting(index, word, count, positions[word])
            self.map[word].append(posting)
        
    """
    def print_index(self, file, size):
        f = open('M1_Report.txt', 'a+')
        f.write("total_unique_tokens: " + str(len(self.map))+ '\n')
        f.write("total_unique_documents: " + str(size) + '\n')
        f.write("total_disk_size: " + str(sys.getsizeof(self.map)) + '\n')
        for word, posting in self.map.items():
            print(word + str( [p.get_posting() for p in posting]))

        f.close()
    """

    def save_dictionary(self, file1, file2):
        """ save the dictionary on outside file """
        np.save(file1, self.map) 
        np.save(file2, self.map_doc_id)




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
        return [self.id, self.score, self.position]
        




