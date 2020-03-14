
from Indexer import *
from QueryProcessor import QueryProcessor 
import numpy as np
import math
import time
from nltk.stem import PorterStemmer
from string import ascii_lowercase

if __name__ == "__main__":
    
    
    index = Indexer()
    #index.start_index()

    query = input("Enter query: ")
    start_time = time.time() #Return the time to start the search 
    qp = QueryProcessor() 
    urlid = qp.search(query.lower())
    temp = []
    if not urlid:
        print('no url find with given query')
    else:
        with open('doc_id.json', 'r') as url_id:
            url_dict = json.load(url_id, strict=False)
        index = 1
        for i in urlid:
            try:
                if index > 20:
                    break
                result_str = "#%3d: %s" %(index,url_dict[str(i)])
                print(result_str)
                index += 1
            except:
                pass
    total_time = time.time() - start_time #The total time used to complete the search
    time_str = "The search took time %f seconds" % (total_time)
    print(time_str)
