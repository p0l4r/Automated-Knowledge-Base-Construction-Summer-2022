'''
Created on Nov 8, 2019
Sample structure of run file run.py

@author: cxchu
'''
import sys
import pandas as pd
import os
import nltk
import csv
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

'''
Some helper functions to get the job done
'''

def process_sentence(sent):
    index = sent.find(' is ')
    if index == -1:
        index = sent.find(' was ')
        if index == -1:
            index = sent.find(' were ')
            if index == -1:
                return sent
            else:
                return sent[index:]
        else:
            return sent[index:]
    else:
        return sent[index:]

def what_is_your_entity_type(sent,entity):
    tokenized_sent = nltk.word_tokenize(sent)
    pos_tag_sent = nltk.pos_tag(tokenized_sent)
    grammar = r""" 
    NBAR:
        {<N.*>*<N.*>}  

    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}
  """ 
    cp = nltk.RegexpParser(grammar)
    noun_phrases_list = [' '.join(leaf[0] for leaf in tree.leaves()) 
                      for tree in cp.parse(pos_tag_sent).subtrees() 
                      if (tree.label()=='NP')]
    try:
        return noun_phrases_list[0]
    except IndexError:
        no_way_but_to_guess = list(entity.split(' '))
        length = len(no_way_but_to_guess)
        return no_way_but_to_guess[length-1]
    

def trying_out_some_more_rules(entity_info):
        if (entity_info == "species") or (entity_info == "moth") or ("organism" in entity_info):
         entity_info = "taxon"
        elif "film" in entity_info:
            entity_info = "film"
        elif ("footballer" in entity_info) or ("soccer player" in entity_info):
            entity_info = "association football player"
        elif "actress" in entity_info or "actor" in entity_info or "model" in entity_info:
            entity_info = "actor"
        elif "football club" in entity_info:
            entity_info = "association football club"
        elif "cricketer" in entity_info:
            entity_info = "cricketer"
        elif "politician" in entity_info:
            entity_info = "politician"
        elif "surname" in entity_info:
            entity_info = "family name"
        elif "game" in entity_info:
            entity_info = "video game"
        elif entity_info == "village":
            entity_info = "human settlement"
        elif "physicist" in entity_info:
            entity_info = "physicist"
        else:
            pass
        
        return entity_info


def your_typing_function(input_file, result_file):
    
    '''
    This function reads the input file (e.g. test.tsv)
    and does typing all given entity mentions.
    The results is saved in the result file (e.g. results.tsv)
    '''
    if os.path.exists('results.tsv'):
        os.remove('results.tsv')

    # dataframe
    df = pd.read_csv(input_file, sep='\t', header=None, names=['entity', 'sentence'])

    for i, row in df.iterrows():
        sent = row['sentence']
        entity = row['entity']
        sent = process_sentence(sent)
        sent = sent.replace(" is ", "")
        sent = sent.replace(" was ", "")
        sent = sent.replace(" were ", "")
        sent = sent.lower() 
        entity_info = what_is_your_entity_type(sent,entity)
        entity_info = trying_out_some_more_rules(entity_info)
        row_to_write = [i, [f'{entity_info}']]
        # if results.tsv exists delete the file
        # write to tsv
        with open(result_file, 'a', encoding='utf-8') as f:
            # without newline
            writer = csv.writer(f, delimiter='\t', lineterminator='\n')
            writer.writerow(row_to_write) 
    
    
'''
*** other code if needed
'''    
    
'''
main function
'''

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('Expected exactly 2 argument: input file and result file')
    your_typing_function(sys.argv[1], sys.argv[2])
    
