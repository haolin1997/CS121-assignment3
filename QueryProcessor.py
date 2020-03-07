from Indexer import *
import numpy as np
import pickle
import json

class QueryProcessor():
    """ a query processor
        take the npy file and read it
        take the query words and process the query using the file
        each time after processing the query, create a QueryResult object
        and store them in all_result
    """ 


    def __init__(self, id_file, index_file):
        """ format of dictionaries: 
                self.doc_id: "doc_id": "url"
                self.index: "word": [Posting Objects]  """

        self.doc_id = np.load(str(id_file),allow_pickle='TRUE').item()
        self.index =  np.load(str(index_file), allow_pickle='TRUE').item()
        with open('doc_id.txt', 'w') as json_file:
            json.dump(self.doc_id, json_file)
        with open('index.txt','w') as json_file:
            json.dump(self.index, json_file)
   
        self.all_results = {}
    

    def search(self,words):
        """ the search component
            print out the results for this query
        """
        words = words.split()
        for word in words:
            result = self._process(word)
        

        sorted_dict = sorted(self.all_results.items(), key=lambda item: item[1], reverse=True)
 
        i = 0
        for doc in sorted_dict[0:5]:        
            print(str(self.doc_id[doc[0]]) + ' ' + str(doc[1]) + '\n' )



    def _process(self,words):
        """ get the query words as a list 
            process the query words, add result to all_result list
            return this single result as a result object
        """
        result = QueryResult(words)
        for i in self.index[words]:

            temp_posting = i.get_posting()
            current_url_id = temp_posting[0]
            current_word_score = temp_posting[1]

            if self.all_results == {}:
                result.add_dict(current_url_id,current_word_score)
            else:
                if current_url_id in self.all_results:
                    result.add_dict(current_url_id, current_word_score)
                    
        self.all_results = result.get()
        
        return result

    
    def clear(self):
        """ delete all the previous results """
        self.all_results = []



class QueryResult():
    """ a query result object can store one result for one single query
        attributes:
            query words: [list of query words]
            files: [list of docs that match the query words] """

    def __init__(self, words):
        """ initialization take the query word as input """
        self.query_words = words
        self.result = list()
        self.result_dict = {}
    
    def add(self, doc_id):
        """ add the doc_id into results list"""
        self.result.append(doc_id)
    
    def add_dict(self, doc_id, score):
        """ add the score to the url """
        if doc_id in self.result_dict:
            self.result_dict[doc_id] += score
        else:
            self.result_dict[doc_id] = score

    def get(self):
        """ get the results as a list """
        return self.result_dict

    
