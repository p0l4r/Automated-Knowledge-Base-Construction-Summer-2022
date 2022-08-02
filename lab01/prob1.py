import os
import spacy
from collections import Counter
import csv
import shutil
import regex as re


def createCSV(header, data, filename):
    try:
        with open(f'{filename}.csv', 'w', newline='',  encoding='UTF8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(header)
            writer.writerows(data)
        print(f"{filename}.csv has been created")
    except FileExistsError:
        print(f"{filename}.csv already exists")
        print("Please delete the file inside Problem1 dir and try again !!!")

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

def unique_NER_frequency_counter(filename):
    NER = spacy.load("en_core_web_sm")
    title = open(filename, encoding="utf8").readline()
    title = title.strip('\n')
    file_text = open(filename, encoding="utf8").read()
    cleaned_file_text = cleanData(file_text)
    doc = NER(cleaned_file_text)

    ent_text_list = [ent.text for ent in doc.ents]
    uNER_data = Counter(ent_text_list)
    header = ["Title", "Named-entity", "Frequency"]
    data = []
    for key, value in uNER_data.items():
        data.append([title, key, value])
    
    createCSV(header, data, title)
    csv_filepath = "./" + title + ".csv"
    return csv_filepath
    
        

if __name__ == "__main__":
    try:
        os.mkdir("Problem1")
    except FileExistsError:
        pass
    
    for file in os.listdir(".\data"):
        if file.endswith(".txt"):
            filename = str(os.path.join("/data", file))
            filename = filename.replace("/", "./")
            filename = filename.replace("\\", "/")    
            csv_filepath = unique_NER_frequency_counter(filename)
            shutil.move(csv_filepath, f"./Problem1/{csv_filepath.strip('./')}")