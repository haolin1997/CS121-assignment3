import numpy as np

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
        self.all_results = list()
    

    def search(self,words):
        """ the search component
            print out the results for this query
        """
        result = self._process(words)
        for doc in result.get():
            print(str(self.doc_id[doc]) + '\n' )


    def _process(self,words):
        """ get the query words as a list 
            process the query words, add result to all_result list
            return this single result as a result object
        """
        result = QueryResult(words)

        





        self.all_results.append(result) 
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
    
    def add(self, doc_id):
        """ add the doc_id into results list"""
        self.result.append(doc_id)

    def get(self):
        """ get the results as a list """
        return self.result

    
