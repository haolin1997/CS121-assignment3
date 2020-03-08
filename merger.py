import json

if __name__ == "__main__":
    
    file_num = 13

    docs = [None] * 13
    tokens = [None] * 13

    fp = [open("inverted_index_%s.txt"%x, 'r') for x in range(0,file_num)]
    
    index = 0
    while index < 1:

        docs[index] = fp[index].readline()
        
        tokens[index] = json.dumps(fp[index])
        index += 1

    print(docs)

        #new_dict = defaultdict
    