
import Indexer as INDEX
import QueryProcessor as QP
import numpy as np




if __name__ == "__main__":
    
    
    index = InvertedIndex()
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
    doc_id_dict = np.load('my_file_doc.npy',allow_pickle='TRUE').item()
    word_dict = np.load('my_file.npy', allow_pickle='TRUE').item()
    
    print(word_dict['learning'][0].get_posting())
    '''
    words = ['machine', 'learning']
    result_temp = []
    result = []

    for i in word_dict[words[0]]:
        result_temp.append(i.get_posting()[0])

    for j in word_dict[words[1]]:
        temp = j.get_posting()[0]
        if temp in result_temp:
            result.append(temp)


    for i in range(len(result)):
        print(doc_id_dict[result[i]])
    '''