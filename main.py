
from Indexer import *
from QueryProcessor import QueryProcessor 
import numpy as np
import math
import time
from nltk.stem import PorterStemmer
from string import ascii_lowercase


if __name__ == "__main__":
    
    
    index = Indexer()
    index.start_index()
    
    """
    query = input("Enter query: ")
    start_time = time.time() #Return the time to start the search 
    qp = QueryProcessor() 
    urlid = qp.search(query)
    url_dict = {}
    if not urlid:
        print('no url find with given query')
    else:
        with open('doc_id.txt', 'r') as url_id:
            url_dict = json.load(url_id, strict=False)
        for i, j in enumerate(urlid):
            result_str = "#%d: %s %s" %(i+1,url_dict[str(j[0])], str(j[1]))
            print(result_str)
    
    total_time = time.time() - start_time #The total time used to complete the search
    time_str = "The search took time %f seconds" % (total_time)
    print(time_str)
    """