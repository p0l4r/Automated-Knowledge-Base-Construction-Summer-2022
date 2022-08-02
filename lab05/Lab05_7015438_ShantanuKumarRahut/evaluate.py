'''
Created on Nov 25, 2019

@author: cxchu
'''

import codecs
import sys
import csv

from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 

def extract_value(str, key):
    res = []
    if key == 'birth':
        res = [val[1:-1].split('-')[0] if val != '' else None for val in str[1:-1].split(', ')]
    else:
        res = [val[1:-1] if val != '' else None for val in str[1:-1].split(', ')]
    return res

##open results file  
def openFile(file):
    res = {}
    with open(file, 'r', encoding='utf8') as fres:
        reader = csv.reader(fres)
        for data in reader:
            if len(data) < 1:
                continue
            if data[0] == 'entity':
                pass
            
            values = {}
            
            values['birth'] = extract_value(data[1], 'birth')
            values['nation'] = extract_value(data[2], 'other')
            values['alma'] = extract_value(data[3], 'other')
            values['award'] = extract_value(data[4], 'other')
            values['work'] = extract_value(data[5], 'other')
            res[data[0]] = values
        return res

'''
toLowerCase() on types
'''
def listToSetNormalization(values):
    res = set()
    for l in values:
        res.add(l.lower() if l is not None else None)
    return res
    

'''
evaluate the results on each property:
The scores include macro and micro, similarly to the entity typing problem
refered in: Ling, Xiao, and Daniel S. Weld. "Fine-grained entity recognition." AAAI, 2012.
'''
def evaluate_property(gtValues, pValues, key):
    
    size = len(gtValues)
    
    macroPre = 0 ; macroRec = 0 ; microCount = 0 ; rCount = 0 ; pCount = 0
    for entity, values in gtValues.items():
        # ------- resume here
        pValues_ent = pValues[entity][key] if entity in pValues and key in pValues[entity] else []
        
        gtlabels = set() ; plabels = set()
        
        gtlabels = listToSetNormalization(values[key])
        plabels = listToSetNormalization(pValues_ent)
        
        TP = gtlabels & plabels
        tmpPre = 0.0
        if len(plabels) != 0:
            tmpPre = len(TP) / len(plabels)
            
        tmpRec = len(TP) / len(gtlabels)
        
        macroPre += tmpPre
        macroRec += tmpRec
        
        microCount += len(TP)
        rCount += len(gtlabels)
        pCount += len(plabels)
        
    macroPre = macroPre / size
    macroRec = macroRec / size
    macrof1 = 0.0
    if (macroPre + macroRec) != 0:
        macrof1 = 2 * macroPre * macroRec / (macroPre + macroRec)
    microPre = microCount/pCount
    microRec = microCount/rCount
    microf1 = 0.0
    if (microPre + microRec) != 0:
        microf1 = 2 * microPre * microRec / (microPre + microRec);
    
    print('Results on extracting ' + key + ':')    
    print('\tMacro Precision, Recall and F1:\t' + str(macroPre) + '\t' + str(macroRec) + '\t' + str(macrof1))
    print('\tMicro Precision, Recall and F1:\t' + str(microPre) + '\t' + str(microRec) + '\t' + str(microf1))
    return macroPre, macroRec, macrof1

def evaluate(pFile, gtFile):
    pRes = openFile(pFile)
    gtRes = openFile(gtFile)
    
    p1, r1, f1 = evaluate_property(gtRes, pRes, 'birth')
    p2, r2, f2 = evaluate_property(gtRes, pRes, 'nation')
    p3, r3, f3 = evaluate_property(gtRes, pRes, 'alma')
    p4, r4, f4 = evaluate_property(gtRes, pRes, 'award')
    p5, r5, f5 = evaluate_property(gtRes, pRes, 'work')
    
    print('\n\nAverage results of all relations:')
    avgP = (p1 + p2 + p3 + p4 + p5)/5
    avgR = (r1 + r2 + r3 + r4 + r5)/5
    avgF = (f1 + f2 + f3 + f4 + f5)/5
    print('\tMacro Precision, Recall and F1:\t' + str(avgP) + '\t' + str(avgR) + '\t' + str(avgF))
   

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('Expected exactly 2 argument: predicted type file and groundtruth type file')
    evaluate(sys.argv[1], sys.argv[2])

