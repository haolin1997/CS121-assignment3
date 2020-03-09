
from Indexer import *
from QueryProcessor import QueryProcessor 
import numpy as np
import math
from nltk.stem import PorterStemmer
from string import ascii_lowercase


if __name__ == "__main__":
    
    
    #index = Indexer()
    #index.start_index()
    
    
    query = input("Enter query: ")
    qp = QueryProcessor()
    urlid = qp.search(query)
    url_dict = {}
    with open('doc_id.txt', 'r') as url_id:
        url_dict = json.load(url_id, strict=False)
    for i in urlid:
        print(url_dict[str(i[0])],i[1])
    #print(PorterStemmer().stem('played'))
    
