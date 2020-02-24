from collections import defaultdict
import json
from bs4 import BeautifulSoup
import os



class InvertedIndex():
    def __init__(self):
        self.map = defaultdict(list)
    
    def fetch_content(self, json_string):
        """ fetch contents from given json string
            store them in the index map """
        json_object = json.loads(json_string)
        #json_object = json_string 
        url = json_object['url']
        html = json_object['content']
        fd = FetchData(html)
        words = fd.get_words()
        for word, count in words.items():
            posting = Posting(url, word, count)
            self.map[word].append(posting)

    def print_index(self, file, size):
        """ print out the index """
        f = open('M1_Report.txt', 'a+')
        f.write("total_unique_tokens: " + str(len(self.map))+ '\n')
        f.write("total_unique_documents: " + str(i) + '\n')
        #for word, posting in self.map.items():
            #print(str([p.get_posting() for p in posting]))

        f.close()


class Posting():
    """ the posting object. 
        It has three arrtibute: the docID;
        the word this posting object related to; the word counts
    """
    def __init__(self,id, word, word_counts):
        self.id = id
        self.word = word
        self.score = word_counts  

    def get_posting(self):
        """ return the content of the posting object as a list
            [docID, score]
        """
        return [self.id, self.score]
        



class FetchData():
    def __init__(self, html):
        self.html = html
        self.word_dict = defaultdict(int)
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
        for line in text:
            if line != '\n':
                line = self._decode_line(line.lower())
                for word in line.split():
                    if self._is_valid_word(word):
                        #self.word_list.append(word)
                        self.word_dict[word] += 1
        
    def get_words(self):
        """ return all the words in this page as a dict"""
        return self.word_dict


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

    #json_file = '{"url": "https://www.cs.uci.edu/event/c-mohan-2/?ical=1", "content": "BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Department of Computer Science - Donald Bren School of Information &amp; Computer Sciences - ECPv4.6.14.1//NONSGML v1.0//EN\r\nCALSCALE:GREGORIAN\r\nMETHOD:PUBLISH\r\nX-WR-CALNAME:Department of Computer Science - Donald Bren School of Information &amp; Computer Sciences\r\nX-ORIGINAL-URL:https://www.cs.uci.edu\r\nX-WR-CALDESC:Events for Department of Computer Science - Donald Bren School of Information &amp; Computer Sciences\r\nBEGIN:VEVENT\r\nDTSTART;VALUE=DATE:20150501\r\nDTEND;VALUE=DATE:20150502\r\nDTSTAMP:20191013T140443\r\nCREATED:20180501T070348Z\r\nLAST-MODIFIED:20180501T070927Z\r\nUID:1491-1430438400-1430524799@www.cs.uci.edu\r\nSUMMARY:C. MOHAN\r\nDESCRIPTION:Speaker: C. MOHAN (IBM Almaden Research Center) \\nHost: Michael Carey & Sharad Mehrotra \\nTitle: Big Data: Hype and Reality & Modern Database Systems: Modernized Classic Systems\\, NewSQL and NoSQL \\n\r\nURL:https://www.cs.uci.edu/event/c-mohan-2/\r\nCATEGORIES:Distinguished Lecture Series\r\nEND:VEVENT\r\nEND:VCALENDAR", "encoding": "ascii"}'
    #index.fetch_content(json_file)
    i = 0
    for directory in os.listdir('DEV'):
        if directory != '.DS_Store':
            for filenames in os.listdir('DEV/' + directory):
                path = 'DEV/'+ directory + '/' + filenames
                json_file = open(path).readlines()[0]
                print(path)
                index.fetch_content(json_file)
                i += 1
    
    f = open('M1_Report.txt', 'w')
    index.print_index('M1_Report.txt', i)
    