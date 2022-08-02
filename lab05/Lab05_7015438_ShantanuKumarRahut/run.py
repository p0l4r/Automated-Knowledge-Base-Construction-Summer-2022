'''
Created on Nov 25, 2019
Sample structure of run file run.py

@author: cxchu
@editor: ghoshs
'''

import sys
import csv
import spacy


def your_extracting_function(input_file, result_file):
    
    '''
    This function reads the input file (e.g. input.csv)
    and extracts the required information of all given entity mentions.
    The results is saved in the result file (e.g. results.csv)
    '''
    with open(result_file, 'w', encoding='utf8') as fout:
        headers = ['entity','dateOfBirth','nationality','almaMater','awards','workPlaces']
        writer = csv.writer(fout, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        
        with open(input_file, 'r', encoding='utf8') as fin:
            reader = csv.reader(fin)

            # skipping header row
            next(reader)
            
            for row in reader:
                entity = row[0]
                abstract = row[1]
                dateOfBirth, nationality, almaMater, awards, workPlace = [], [], [], [], []
                
                '''
                baseline: adding a random value 
                comment this out or remove this baseline 
                '''
                # dateOfBirth.append('1961-1-1')
                # nationality.append('United States')
                # almaMater.append('Johns Hopkins University')
                # awards.append('Nobel Prize in Physics')
                # workPlace.append('Johns Hopkins University')
                
                '''
                load spacy NER model
                '''
                nlp = spacy.load('en_core_web_sm')
                doc = nlp(abstract)
                
                '''
                extracting information 
                '''

                dateOfBirth += extract_dob(doc)
                nationality += extract_nationality(doc)
                almaMater += extract_almamater(doc)
                awards += extract_awards(doc)
                workPlace += extract_workpace(doc)
                
                writer.writerow([entity, str(dateOfBirth), str(nationality), str(almaMater), str(awards), str(workPlace)])
        
    
'''
date of birth extraction funtion
'''
def month_to_number(month):
    '''
    This function converts the month to the number
    param: 
    month = string of month
    output: 
    month = integer of month
    '''
    dict_month = {
        "January": "01",
        "February":"02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12"
    }
    return dict_month[month]

def dob_formatter(dob):
    '''
    This function formats the date of birth to the format YYYY-MM-DD
    param: 
    date = string of date of birth
    output: 
    date = string of date of birth in the format YYYY-MM-DD
    '''
    dob = dob.replace(",", " ")
    year = 0
    month = 0
    date = 0
    dob = dob.split(" ")
    for any_part in dob:
        if any_part in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]:
            month = month_to_number(any_part)
            if str(month) == "0":
                month = "01"
        elif any_part.isdigit():
            if int(any_part) > 31:
                year = int(any_part)
            else:
                date = int(any_part)
                if date < 10 and date > 0:
                    date = "0" + str(date)
    
    return str(year) + "-" + str(month) + "-" + str(date)

def extract_dob(doc):
    dob = []
    '''
    === your code goes here ===
    '''
    # extract date of birth for entity from the abstract
    for ent in doc.ents:
        if ent.label_ == "DATE":
            formatted_text = dob_formatter(ent.text)
            if formatted_text == "0-0-0":
                continue
            else:
                dob.append(formatted_text)
                break
        else:
            pass
    
    return dob


'''
nationality extraction function
'''
def some_rules_for_nationality(text):
    if text == "American" or text == "U.S." or text == "U.S.A." or text == "U.S.A." or text == "USA" :
        return "United States"
    elif text == "British" or text == "England" or text == "English":
        return "United Kingdom"
    elif text == "French" or text == "France":
        return "France"
    elif text == "German" or text == "Germany":
        return "Germany"
    elif text == "Australian":
        return "Australia"
    elif text == "Canadian":
        return "Canada"
    elif text == "Italian":
        return "Italy"
    elif text == "Spanish":
        return "Spain"
    elif text == "Swedish":
        return "Sweden"
    elif text == "Swiss":
        return "Switzerland"
    elif text == "Indian":
        return "India"
    elif text == "Chinese":
        return "China"
    elif "Auckland" in text:
        return "Auckland"
    elif text == "Israeli" or text == "Jerusalem" or text == "Jewish":
        return "Israel"
    elif text == "Japanese":
        return "Japan"
    elif text == "Russian" or text == "Soviet":
        return "Russia"
    elif text == "Korean":
         return "Korea"
    elif text == "Mexican":
        return "Mexico"
    elif text == "Brazilian":
        return "Brazil"
    elif text == "Argentine":
        return "Argentina"
    elif text == "Polish":
        return "Poland"
    elif text == "Portuguese":
        return "Portugal"
    elif text == "Romanian":
        return "Romania"
    elif text == "Turkish":
        return "Turkey"
    elif text == "Vietnamese":
        return "Vietnam"
    elif text == "Indonesian":
        return "Indonesia"
    elif text == "Pakistani":
        return "Pakistan"
    elif text == "Greek":
        return "Greece"
    elif text == "Austrian":
        return "Austria"
    else:
        return text
    

def extract_nationality(doc):
    nationality = []
    '''
    === your code goes here ===
    '''
    for ent in doc.ents:
        if ent.label_ == "NORP":
            formatted_text = some_rules_for_nationality(ent.text)
            nationality.append(formatted_text)
            break
        else:
            pass
    return nationality
 

'''
alma mater extraction function
'''
def extract_almamater(doc):
    almaMater = []
    '''
    === your code goes here ===
    '''
    # extract alma mater for entity from the abstract
    for ent in doc.ents:
        if ent.label_ == "ORG":
            if "University" in ent.text or "College" in ent.text or "School" in ent.text:
                almaMater.append(ent.text)
            elif "university" in ent.text or "college" in ent.text or "school" in ent.text:
                almaMater.append(ent.text)
            else:
                 pass
        else:
            pass
                
    return almaMater


'''
awards extracttion function
'''
def clean_awards_data(awards):
    awards = [x.lower() for x in awards]
    awards = [x.replace("the", "") for x in awards]
    awards = [x.replace("(", "") for x in awards]
    awards = [x.replace(")", "") for x in awards]
    
    return awards

def extract_awards(doc):
    awards = []
    '''
    === your code goes here ===
    '''
    # extract awards for entity from the abstract
    # find the entity in the abstract
    for ent in doc.ents:
        if "award" in ent.text or "Award" in ent.text or "grant" in ent.text or "Grant" in ent.text or "scholarship" in ent.text or "Scholarship" in ent.text or "prize" in ent.text or "Prize" in ent.text:
            awards.append(ent.text)
        elif "medal" in ent.text or "Medal" in ent.text or "honor" in ent.text or "Honor" in ent.text or "fellowship" in ent.text or "Fellowship" in ent.text:
            awards.append(ent.text)
        elif "achievement" in ent.text or "Achievement" in ent.text  or "achieve" in ent.text or "Achieve" in ent.text:
            awards.append(ent.text)
        elif "fellow" in ent.text or "Fellow" in ent.text or "fellowship" in ent.text or "Fellowship" in ent.text:
            awards.append(ent.text)
        elif "medallion" in ent.text or "Medallion" in ent.text or "medal" in ent.text or "Medal" in ent.text:
            awards.append(ent.text)
        elif "gold" in ent.text or "Gold" in ent.text or "silver" in ent.text or "Silver" in ent.text or "bronze" in ent.text or "Bronze" in ent.text:
            awards.append(ent.text)
        elif "padma" in ent.text or "Padma" in ent.text:
            awards.append(ent.text)
        elif "distinction" in ent.text or "Distinction" in ent.text:
            awards.append(ent.text)
        elif "Association" in ent.text or "association" in ent.text:
            awards.append(ent.text)
        else:
            if ent.label == "ORG":
                awards.append(ent.text)
    awards = clean_awards_data(awards)
    return awards



'''
workplace extraction function
'''
def extract_workpace(doc):
    workPlace = []
    '''
    === your code goes here ===
    '''
    for ent in doc.ents:
        if ent.label_ == "ORG":
            if "Medal" not in ent.text or "Award" not in ent.text:
                workPlace.append(ent.text)
        else:
            pass

    return workPlace


'''
main function
'''
if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('Expected exactly 2 argument: input file and result file')
    your_extracting_function(sys.argv[1], sys.argv[2])
    # print(dob_formatter("January 1, 2000"))
