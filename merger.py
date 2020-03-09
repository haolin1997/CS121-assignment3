import json
import math
from collections import defaultdict

TOTAL_UNIQUE_DOC = 55392

def tf_idf_score(tokens):

    for token in tokens.keys():
        df = len(tokens[token])
        idf = math.log(TOTAL_UNIQUE_DOC/df)
        for posting in tokens[token]:
            tf = posting[1]
            tf_idf = (1 + math.log(tf)) * idf
            posting[1] = tf_idf
    
    return tokens

def write_full_index(tokens):

    with open("full_index.txt", "a") as f:
        json.dump(tokens, f)
        f.write("\n")

if __name__ == "__main__":
    
    file_num = 13

    docs = [None] * 13
    tokens = [None] * 13

    merged_dict = defaultdict(list)

    fp = [open("inverted_index_%s.txt"%x, 'r') for x in range(0,file_num)]
    
    index = 0
    while index < file_num:

        docs[index] = fp[index].readline()
        
        tokens[index] = json.loads(docs[index])
        index += 1

    tf_idf_score(tokens[0])

    valid_i = [x for x in range(0, file_num)]

    
    while True:
        
        token = min(list(tokens[x].keys())[0] for x in valid_i)
        
        new_dict = defaultdict(list)

        for index in valid_i:
            if list(tokens[index].keys())[0] == token:
                for element in tokens[index][token]:
                    new_dict[token].append(element)
                    #print(new_dict[token])
                #read next line of the partial index
                docs[index] = fp[index].readline()
                if not docs[index]:
                    valid_i.remove(index)
                    fp[index].close()
                else:
                    tokens[index] = json.loads(docs[index])
        
        new_dict = tf_idf_score(new_dict)
  
        write_full_index(new_dict)

        if not valid_i:
            break
                    
        #new_dict = defaultdict
    