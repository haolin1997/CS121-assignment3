from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()

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
        important = []
        # ===== beautiful soup ====
        soup = BeautifulSoup(self.html,'html.parser')
       
        for script in soup(["script","style"]): 
            script.extract()
        text = soup.get_text()
    
        # =========================
        important = self.get_important_words(soup, important)

        text = text.split(" ")
        i = 0
        for line in text:
            if line != '\n':
                line = self._decode_line(line.lower())
                for word in line.split():
                    if self._is_valid_word(word):
                        #print(word)
                        if ps.stem(word).isalnum():
                            word = ps.stem(word)
                            i += 1
                            self.word_dict[word] += 1
                        if word in important:
                            self.word_dict[word] *= 2
                        #If it is an important word, add more weights to it
                        #if word not in self.position_dict.keys():
                         #   self.position_dict[word] = [i]
                        #else:
                         #   self.position_dict[word].append(i)
    
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