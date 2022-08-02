'''
Created on Nov 25, 2019
Sample structure of run file run.py

@author: cxchu
'''

import sys
import spacy

nlp = spacy.load("en_core_web_sm")


def your_extracting_function(input_file, result_file):
    
    '''
    This function reads the input file (e.g. sentences.tsv)
    and extracts all SPO per line.
    The results are saved in the result file (e.g. results.txt)
    '''
    with open(result_file, 'w', encoding='utf8') as fout:
        with open(input_file, 'r', encoding='utf8') as fin:
            id = 1
            for line in fin:
                line = line.rstrip()
                
                '''
                baseline: running dependency, return head verb, nominal subject and directed object
                comment out or remove when running your code
                verbs = {key: {'subject': text, 'object': text}}
                '''
                
                # verbs = spo_baseline(line)
                        
                '''
                end baseline
                '''

                '''
                Extracting SPO
                === your code goes here ===
                '''
                verbs = my_spo_extracting_function(line)
                

                '''
                formatting dict compatible with oie reader
                '''
                if len(verbs) > 0:
                    res = ''
                    for key, value in verbs.items():
                        if value['subject'] != '' and value['object'] != '':
                            res += str(id) + '\t"' + value["subject"] + '"\t"' + key + '"\t"' + value["object"] + '"\t0\n'
                        elif value['subject'] == '' and value['object'] != '':
                            res += str(id) + '\t"' + " " + '"\t"' + key + '"\t"' + value["object"] + '"\t0\n'
                        elif value['subject'] != '' and value['object'] == '':
                            res += str(id) + '\t"' + value["subject"] + '"\t"' + key + '"\t"' + " " + '"\t0\n'
                        else:
                            continue
                            
                    if res != '':
                        fout.write(line + "\n")
                        fout.write(res) 
                        id += 1


'''
baseline implementation
'''
def spo_baseline(line):
    verbs = {}
    doc = nlp(line)
    for token in doc:
        key=token.head.text;
        if(token.head.pos_ == "VERB" and key not in verbs.keys()):
            verbs[key] = {"subject":"","object":""};
        if(token.dep_ == "nsubj" and token.head.pos_ == "VERB"):
            verbs[key]["subject"] = token.text;
            
        elif(token.dep_ == "dobj" and token.head.pos_ == "VERB"):
            verbs[key]["object"] = token.text;
    return verbs


    
'''
*** other code if needed
'''    

def my_spo_extracting_function(line):
    # extract subject , predicate and object
    # return a dict with key as predicate and value as a dict with subject and object
    SUBJECTS = {"nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"}
    OBJECTS = {"dobj", "dative", "attr", "oprd","iobj"}
    
    doc = nlp(line)
    verbs = {}
    for token in doc:
        if token.dep_ in SUBJECTS:
            key=token.head.text
            if(key not in verbs.keys()):
                verbs[key] = {"subject":"","object":""}
            verbs[key]["subject"] = token.text
        elif token.dep_ in OBJECTS:
            key=token.head.text
            if(key not in verbs.keys()):
                verbs[key] = {"subject":"","object":""}
            verbs[key]["object"] = token.text
    return verbs
    
'''
main function
'''
if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('Expected exactly 2 argument: input file and result file')
    your_extracting_function(sys.argv[1], sys.argv[2])
