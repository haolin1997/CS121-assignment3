from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import hashlib

ps = PorterStemmer()

class DataFetcher():
    """ this class fetch words from html 
        and build dictionaries to store resulted information
    """
    def __init__(self, html):
        self.html = html
        self.word_dict = defaultdict(int)
        self.biword_dict = defaultdict(int)
        self.triword_dict = defaultdict(int)
        self.position_dict = defaultdict(list)
        self.checksum = 0
        self.fetch()
       


    def fetch(self):
        """ fetch html data and parse 
            store resulted words in:
                words_dict, formatting as "word": count 
                position_dict, "word": [list of positions]
        """
        # ===== beautiful soup ====
        important = []
        soup = BeautifulSoup(self.html,'html.parser')
        for script in soup(["script","style"]): 
            script.extract()
        #print(soup.find('a')['href'])
        text = soup.get_text()
        ## calculate the check sum
        
        self.checksum = hashlib.md5(text.encode('utf-8')).hexdigest()
        
        text = text.split(" ")
        important = self.get_important_words(soup, important)
        # =========================
        # == building one and two word index dic ==
        for line in text:
            if line != '\n':
                line = self._decode_line(line.lower())
                line = line.split()
                valid_line = []
                for word in line:
                    if self._is_valid_word(word) and ps.stem(word).isalnum():
                        word = ps.stem(word)
                        valid_line.append(word)
                for w in range(len(valid_line)):
                    word = valid_line[w]
                    self.word_dict[word] += 1
                    if word in important:
                        self.word_dict[word] *= 2
                    # biword index
                    if w < len(valid_line)-1:
                        next_word = valid_line[w+1]
                        biword = str(word) + " " + str(next_word)
                        self.biword_dict[biword] += 1
                        if word in important:
                            self.biword_dict[biword] *= 2
                        if next_word in important:
                            self.biword_dict[biword] *= 2       
                    # tri-word index
                    if w < len(valid_line) -2:
                        next_word = valid_line[w+1]
                        next_next_word = valid_line[w+2]
                        tri_word = str(word) + " " + str(next_word) + " " + str(next_next_word)
                        self.triword_dict[tri_word] += 1
                        if word in important:
                            self.triword_dict[tri_word] *= 2
                        if next_word in important:
                            self.triword_dict[tri_word] *= 2
                        if next_next_word in important:
                            self.triword_dict[tri_word] *= 2
      
        # ============================================
          
    def get_important_words(self, soup, important):
        try:
            for word in soup.title.string.split():
                word = word.lower()
                if ps.stem(word) not in important and self._is_valid_word(word):
                    important.append(ps.stem(word))
        except:
            pass
        
        for tags in soup.find_all(["h1", "h2", "h3", "b"]):
            try:
                tag = tags.string.split()
                for text in tag:
                    if ps.stem(word) not in important and self._is_valid_word(word):
                        important.append(ps.stem(word))
            except:
                pass
        
        return important

    def get_words(self):
        """ return all the words in this page as a dict"""
        return self.word_dict

    def get_biwords(self):
        return self.biword_dict

    def get_triwords(self):
        return self.triword_dict

    def get_position(self):
        """ return the position information of all words as a dict"""
        return self.position_dict
    
    def get_checksum(self):
        """return the checksum value"""
        return self.checksum

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

        if len(word) == 1 and word not in one_letter:
            return False
        return True