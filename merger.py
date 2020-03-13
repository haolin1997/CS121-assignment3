import json
import math
from collections import defaultdict

TOTAL_UNIQUE_DOC = 55393

def tf_idf_score(tokens):
    """
    calculate the tf_idf_score for each token
    """
    for token in tokens.keys():
        df = len(tokens[token])
        idf = math.log(TOTAL_UNIQUE_DOC/df)
        for posting in tokens[token]:
            tf = posting[1]
            tf_idf = (1 + math.log(tf)) * idf
            posting[1] = tf_idf
    
    return tokens

def write_full_index(tokens):
    """
    write the full single world index file
    """
    with open("full_index.txt", "a") as f:
        json.dump(tokens, f)
        f.write("\n")

def write_full_index_biword(tokens):
    """
    write the full biword index file
    """
    with open("full_biword_index.txt", "a+") as f:
        json.dump(tokens, f)
        f.write("\n")

def write_full_index_triword(tokens):
    """
    write the full triword index file
    """
    with open("full_triword_index.txt", "a+") as f:
        json.dump(tokens, f)
        f.write("\n")

def merge(filename, mode):
    """
    Merge the inverted index file together
    """
    file_num = 12

    docs = [None] * 12
    tokens = [None] * 12

    fp = [open("%s%s.txt"%(filename,x), 'r') for x in range(0,file_num)]
    
    index = 0
    while index < file_num:

        docs[index] = fp[index].readline()
        
        tokens[index] = json.loads(docs[index])
        index += 1

    valid_i = [x for x in range(0, file_num)]

    
    while True:
        
        token = min(list(tokens[x].keys())[0] for x in valid_i)
        
        new_dict = {token:[]}

        for index in valid_i:
            if list(tokens[index].keys())[0] == token:
                for element in tokens[index][token]:
                    new_dict[token].append(element)
                    
                #read next line of the partial index
                docs[index] = fp[index].readline()
                if not docs[index]:
                    valid_i.remove(index)
                    fp[index].close()
                else:
                    tokens[index] = json.loads(docs[index])
        
        new_dict = tf_idf_score(new_dict)
  
        if mode == 'biword':
            write_full_index_biword(new_dict)
        elif mode == 'reg':
            write_full_index(new_dict)
        elif mode == 'triword':
            write_full_index_triword(new_dict)
        else:
            print("please enter a valid mode")
            break

        if valid_i == []: #If all index file become empty, terminate the while loop 
            break
           


if __name__ == "__main__":
    
    file_num = 12

    docs = [None] * 12
    tokens = [None] * 12

    merge("inverted_biword_index_file/inverted_biword_index_", "biword")
  
    merge("inverted_index_file/inverted_index_", "reg")

    merge("inverted_triword_index_file/inverted_triword_index_", "triword")
        