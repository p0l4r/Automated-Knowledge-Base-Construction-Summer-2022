'''
Created on Nov 8, 2019

@author: cxchu
'''

import codecs
import sys

from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 

##open results file  
def openFile(file):
    res = {}
    for line in codecs.open(file, 'r', encoding='utf'):
        data = line.rstrip().split('\t')
        types = [type[1:-1] if type != '' else None for type in data[1][1:-1].split(', ')]
        res[int(data[0])] = types
    return res

'''
toLowerCase() on types
'''
def listToSetNormalization(labels):
    res = set()
    for l in labels:
        res.add(l.lower() if l is not None else None)
    return res

'''
extract the head word (the last word in the type)
lemmatize the head word
'''
def listToSetHeadWord(labels):
    res = set()
    for l in labels:
        if l is not None and l != '':
            lLower = l.lower()
            lLemma = lemmatizer.lemmatize(lLower.split()[-1])
            res.add(lLemma)
        else:
            res.add(None)
    return res
    

'''
evaluate the results, using two ways:
- Strict: exact matching on the results
- Loose: exact matching on the lemmatized head words of the types
The scores include macro and micro, used in entity typing problem
refered in: Ling, Xiao, and Daniel S. Weld. "Fine-grained entity recognition." AAAI, 2012.
'''
def evaluate(pFile, gtFile, hard):
    pRes = openFile(pFile)
    rRes = openFile(gtFile)
    
    size = len(rRes)
    macroPre = 0 ; macroRec = 0 ; microCount = 0 ; rCount = 0 ; pCount = 0
    for id, rOriLab in rRes.items():
        pOriLab = pRes[id]
        
        rlabels = set() ; plabels = set()
        if hard:
            rlabels = listToSetNormalization(rOriLab)
            plabels = listToSetNormalization(pOriLab)
        else:
            rlabels = listToSetHeadWord(rOriLab)
            plabels = listToSetHeadWord(pOriLab)
            
        
        TP = rlabels & plabels
        
        tmpPre = len(TP) / len(plabels)
        tmpRec = len(TP) / len(rlabels)
        
        macroPre += tmpPre
        macroRec += tmpRec
        
        microCount += len(TP)
        rCount += len(rlabels)
        pCount += len(plabels)
        
    macroPre = macroPre / size
    macroRec = macroRec / size
    
    macrof1 = 2 * macroPre * macroRec / (macroPre + macroRec)
    microPre = microCount/pCount
    microRec = microCount/rCount
    microf1 = 2 * microPre * microRec / (microPre + microRec);
    if hard:
        print('Strict: Using exact matching:')
    else:
        print('Loose: Using exact matching on the lemma of the head-word of the type:')
        
    print('\tMacro Precision, Recall and F1:\t' + str(macroPre) + '\t' + str(macroRec) + '\t' + str(macrof1))
    print('\tMicro Precision, Recall and F1:\t' + str(microPre) + '\t' + str(microRec) + '\t' + str(microf1))    
        


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('Expected exactly 2 argument: predicted type file and groundtruth type file')
    evaluate(sys.argv[1], sys.argv[2], True)
    evaluate(sys.argv[1], sys.argv[2], False)

