
from Indexer import *
from QueryProcessor import QueryProcessor 
import numpy as np




if __name__ == "__main__":
    
    
    index = Indexer()
    '''
    path = '/Users/Frank/Documents/GitHub/CS121-assignment3/DEV/aiclub_ics_uci_edu/8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json'
    json_file = open(path).readlines()[0]
    index.fetch_content(1, json_file)
    index.print_index('M1_Report.txt', 1)
    
    i = 0
    for directory in os.listdir('DEV'):
        if directory != '.DS_Store':
            for filenames in os.listdir('DEV/' + directory):
                path = 'DEV/'+ directory + '/' + filenames
                json_file = open(path).readlines()[0]
                print(path)
                index.fetch_content(i, json_file)
                i += 1
    index.save_dictionary('my_file.npy', 'my_file_doc.npy')
    f = open('M1_Report.txt', 'w')
    index.print_index('M1_Report.txt', i)
    
'''
    
    query = input("Enter query: ")

    qp = QueryProcessor('my_file_doc.npy', 'my_file.npy')

    qp.search(query)
