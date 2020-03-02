from collections import defaultdict
from bs4 import BeautifulSoup

class DataFetcher():
    """ this class fetch words from html 
        and build dictionaries to store resulted information
    """
    def __init__(self, html):
        self.html = html
        self.word_dict = defaultdict(int)
        self.position_dict = defaultdict(list)
        #self.stopword = [word.rstrip('\n') for word in open('StopWord.txt', 'r').readlines()]
        self.stopword = []
        self.fetch()


    def fetch(self):
        """ fetch html data and parse 
            store resulted words in:
                words_dict, formatting as "word": count 
                position_dict, "word": [list of positions]
        """
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
        """ return the position information of all words as a dict"""
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