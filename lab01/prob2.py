import os
from turtle import pos
import spacy
from collections import Counter
import csv
import shutil
import regex as re


def createCSV(data):
    try:
        header = ["Title", "POS Type", "POS", "Frequency"]
        with open('Problem2_1.csv', 'w', newline='',  encoding='UTF8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(header)
            writer.writerows(data)
        print("Problem2_1.csv has been created")
    except FileExistsError:
        print("Problem2_1.csv already exists")
        print("Please delete the file inside Problem2_1 dir and try again !!!")

def createCSV_Problem2_2(header, data, filename):
    try:
        with open(f'{filename}.csv', 'w', newline='',  encoding='UTF8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(header)
            writer.writerows(data)
        print(f"{filename}.csv has been created")
    except FileExistsError:
        print(f"{filename}.csv already exists")
        print("Please delete the file inside Problem2_2 dir and try again !!!")

def cleanData(doc):
    nlp = spacy.load("en_core_web_sm")
    doc = doc.lower()
    doc = re.sub("[^A-Za-z0-9]+"," ",doc)
    doc = nlp(doc)
    tokens = [tokens.lower_ for tokens in doc]
    tokens = [tokens for tokens in doc if (tokens.is_stop == False)]
    tokens = [tokens for tokens in tokens if (tokens.is_punct == False)]
    final_token = [token.lemma_ for token in tokens]
    
    return " ".join(final_token)

def get_verb_and_adjectives(filename):
    nlp = spacy.load("en_core_web_sm")
    title = open(filename, encoding="utf8").readline()
    title = title.strip('\n')
    file_text = open(filename, encoding="utf8").read()
    cleaned_file_text = cleanData(file_text)
    doc = nlp(cleaned_file_text)

    verbs = [token.lemma_ for token in doc if (not token.is_stop and not token.is_punct and token.pos_ == "VERB")]
    adjectives = [token.lemma_ for token in doc if (not token.is_stop and not token.is_punct and token.pos_ == "ADJ")]
    
    most_common_verbs  = dict(Counter(verbs).most_common(5))
    # print(most_common_verbs)
    most_common_adjectives = dict(Counter(adjectives).most_common(5))
    # print(most_common_adjectives)
    
    data = []
    for key, value in most_common_verbs.items():
        data.append([title, "Verb", key, value])
        
    for key, value in most_common_adjectives.items():
        data.append([title, "Adjective", key, value])

    
    return data
    

def sentenceTokenizer(filename):
    nlp = spacy.load("en_core_web_sm")
    title = open(filename, encoding="utf8").readline()
    title = title.strip('\n')
    file_text = open(filename, encoding="utf8").read()
    cleaned_file_text = cleanData(file_text)
    doc = nlp(cleaned_file_text)
    sentences = [sent.text for sent in doc.sents]
    return sentences

def get_sentence_with_unique_named_entity(filename):
    nlp = spacy.load("en_core_web_sm")
    title = open(filename, encoding="utf8").readline()
    title = title.strip('\n')
    file_text = open(filename, encoding="utf8").read()
    cleaned_file_text = cleanData(file_text)
    doc = nlp(cleaned_file_text)
    ent_text_list = [ent.text for ent in doc.ents]
    uNER_data = Counter(ent_text_list)
    uNER = []
    for key, _ in uNER_data.items():
        uNER.append(key)
    
    sentences = sentenceTokenizer(filename)
    
    data = []
    for key, _ in uNER_data.items():
        for sentence in sentences:
            if key in sentence:
                data.append([title, key, sentence])
    
    header = ["Title", "Named-entity", "Sentence"]
    createCSV_Problem2_2(header, data, title)
    csv_filepath = "./" + title + ".csv"
    return csv_filepath

if __name__ == "__main__":
    ## Problem 2_1
    try:
        os.mkdir("Problem2_1")
    except FileExistsError:
        pass
    
    data = []
    for file in os.listdir(".\data"):
        if file.endswith(".txt"):
            filename = str(os.path.join("/data", file))
            filename = filename.replace("/", "./")
            filename = filename.replace("\\", "/")    
            data.extend(get_verb_and_adjectives(filename))
    createCSV(data)
    shutil.move("./Problem2_1.csv", "./Problem2_1/Problem2_1.csv")
    
    ## Problem 2_2
    try:
        os.mkdir("Problem2_2")
    except FileExistsError:
        pass
    
    for file in os.listdir(".\data"):
        if file.endswith(".txt"):
            filename = str(os.path.join("/data", file))
            filename = filename.replace("/", "./")
            filename = filename.replace("\\", "/")    
            csv_filepath = get_sentence_with_unique_named_entity(filename)
            shutil.move(csv_filepath, f"./Problem2_2/{csv_filepath.strip('./')}")