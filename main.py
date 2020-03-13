
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
    #index.fetch_one('DEV/www_ics_uci_edu/c5e335113ce9586786ca7683a414cf6de2521b7789542455375e46ebba2c3ddb.json')
    #index.find_file('https://www.ics.uci.edu/~aburtsev/143A/lectures/lecture03-calling-conventions/')
   
    
    query = input("Enter query: ")
    start_time = time.time() #Return the time to start the search 
    qp = QueryProcessor() 
    urlid = qp.search(query)
    temp = []
    if not urlid:
        print('no url find with given query')
    else:
        #url_id = open('doc_id.txt', 'r').read()
        #url_dict = eval(url_id)
        with open('doc_id.json', 'r') as url_id:
            url_dict = json.load(url_id, strict=False)
        for i, j in enumerate(urlid):
            result_str = "#%3d: %s" %(i+1,url_dict[str(j)])
            print(result_str)
    
    total_time = time.time() - start_time #The total time used to complete the search
    time_str = "The search took time %f seconds" % (total_time)
    print(time_str)
    