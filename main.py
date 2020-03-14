
from Indexer import *
from QueryProcessor import QueryProcessor 
import numpy as np
import math
import time
from nltk.stem import PorterStemmer
from string import ascii_lowercase

def save_doc_id(left):
    """
    save the doc id left
    """
    save_dict = json.dumps(left)
    f = open('doc_id.json', 'w')
    f.write(save_dict)
    f.close()

if __name__ == "__main__":
    
    
    index = Indexer()
    #index.start_index()
    '''
    with open('duplicate.json', 'r') as url_id:
        duplicate = json.load(url_id, strict=False)
    with open('doc_id.json', 'r') as url_id:
        url_dict = json.load(url_id, strict=False)

    for i in duplicate:
        del url_dict[str(i)]
    
    save_doc_id(url_dict)
    '''
    #index.fetch_one('/Users/Frank/Documents/GitHub/CS121-assignment3/DEV/www_stat_uci_edu/0a9a1d7860c7dd3c2207f96754dd4246b42d55199ecf8a4c59aff2ab89b84e22.json')
    #index.find_file('https://cbcl.ics.uci.edu/doku.php/teaching/cs285s14/start?rev=1490826928')
    
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
