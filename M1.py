from collections import defaultdict
import json
from bs4 import BeautifulSoup
import os
import numpy as np
import sys


class InvertedIndex():
    def __init__(self):
        self.map = defaultdict(list)
        self.map_doc_id = defaultdict(list)
    
    def fetch_content(self, index, json_string):
        """ fetch contents from given json string
            store them in the index map """
        json_object = json.loads(json_string)
        #json_object = json_string 
        url = json_object['url']
        html = json_object['content']
        fd = FetchData(html)
        words = fd.get_words()
        positions = fd.get_position()
        self.map_doc_id[index] = url
        for word, count in words.items():
            posting = Posting(index, word, count, positions[word])
            self.map[word].append(posting)
        

    def print_index(self, file, size):
        """ print out the index """
        f = open('M1_Report.txt', 'a+')
        f.write("total_unique_tokens: " + str(len(self.map))+ '\n')
        f.write("total_unique_documents: " + str(size) + '\n')
        f.write("total_disk_size: " + str(sys.getsizeof(self.map)) + '\n')
        for word, posting in self.map.items():
            print(word + str( [p.get_posting() for p in posting]))

        f.close()

    def save_dictionary(self, file1, file2):
        np.save(file1, self.map) 
        np.save(file2, self.map_doc_id)

class Posting():
    """ the posting object. 
        It has three arrtibute: the docID;
        the word this posting object related to; the word counts
    """
    def __init__(self,id, word, word_counts, position):
        self.id = id
        self.word = word
        self.score = word_counts  
        self.position = position

    def get_posting(self):
        """ return the content of the posting object as a list
            [docID, score]
        """
        return [self.id, self.score, self.position]
        



class FetchData():
    def __init__(self, html):
        self.html = html
        self.word_dict = defaultdict(int)
        self.position_dict = defaultdict(list)
        #self.stopword = [word.rstrip('\n') for word in open('StopWord.txt', 'r').readlines()]
        self.stopword = []
        self.fetch()


    def fetch(self):
        """ fetch html data and parse 
            store resulted words in words_dict formatting as [word]: count """
        # ===== beautiful soup ====
        soup = BeautifulSoup(self.html,'html.parser')
        #text = soup.find_all(text=True, script = True)
        for script in soup(["script","style"]): 
            script.extract()
        text = soup.get_text()
        #text = soup.find_all(text=True)
        #text = soup.find_all('div')
        #print (type(text))
        # =========================
    
        text = text.split(" ")
        i = 0
        for line in text:
            if line != '\n':
                line = self._decode_line(line.lower())
                for word in line.split():
                    if self._is_valid_word(word):
                        i += 1
                        self.word_dict[word] += 1
                        if word not in self.position_dict.keys():
                            self.position_dict[word] = [i]
                        else:
                            self.position_dict[word].append(i)
        
    def get_words(self):
        """ return all the words in this page as a dict"""
        return self.word_dict

    def get_position(self):
        return self.position_dict

    def _decode_line(self, line):  
        for c in line:
            if not c.isascii():
                line = line.replace(c, " ") #check if it's ascii
            if 32 < ord(c) < 65:
                line = line.replace(c, " ") #check if it's #$%^
            #if 57 < ord(c) < 65:
            #    line = line.replace(c, " ")
            if 90 < ord(c) < 97:
                line = line.replace(c, " ")
            if 122 < ord(c) < 127:
                line = line.replace(c, " ")
        return line
    
    def _is_valid_word(self, word):
        one_letter = ["i", "a"]
        if word in self.stopword:
            return False
        if len(word) == 1 and word not in one_letter:
            return False
        return True



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

