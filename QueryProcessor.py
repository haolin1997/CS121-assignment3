from Indexer import *
import numpy as np
import pickle
import json
from string import ascii_lowercase
from nltk.stem import PorterStemmer
from operator import itemgetter

class QueryProcessor():
    """ a query processor
        take the npy file and read it
        take the query words and process the query using the file
        each time after processing the query, create a QueryResult object
        and store them in all_result
    """ 


    def __init__(self):
        """ format of dictionaries: 
                self.doc_id: "doc_id": "url"
                self.index: "word": [Posting Objects]  """
        self.fp = [open("split_index_%s.txt"%x, 'r') for x in ascii_lowercase]
        self.all_results = {}
        self.urlid = []
    

    def search(self,words):
        """ the search component
            print out the results for this query
        """
        words = words.split()
        for word in words:
            word = PorterStemmer().stem(word)
            fp_num = ord(word[0]) - 97
            self._process(word, fp_num)
        
        self.urlid = sorted(self.all_results.items(), key = lambda kv:kv[1], reverse=True)
        return self.urlid[:20]
        #sorted_dict = sorted(self.all_results.items(), key=lambda item: item[1], reverse=True)
 
        #i = 0
        #for doc in sorted_dict[0:5]:        
            #print(str(self.doc_id[doc[0]]) + ' ' + str(doc[1]) + '\n' )



    def _process(self,word, fp_num):
        """ get the query words as a list 
            process the query words, add result to all_result list
            return this single result as a result object
        """
        #print(fp_num)
        while True:
            
            line = self.fp[fp_num].readline()
            if word in line:
                word_dict = json.loads(line)
                if (list(word_dict.keys())[0]) != word:
                    continue
                for i in (sorted(word_dict[word], key=itemgetter(1), reverse=True)[:75]):
                    if i[0] in self.all_results:
                        self.all_results[i[0]] += i[1]
                    else:
                        self.all_results[i[0]] = i[1]
                break
            if not line:
                break
        
    

    
    def clear(self):
        """ delete all the previous results """
        self.all_results = []



    
