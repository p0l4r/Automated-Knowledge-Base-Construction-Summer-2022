"""
Barebone code created by: Tuan-Phong Nguyen
Date: 2022-06-03
"""

import logging
from typing import Dict, List, Tuple
import spacy
from spacy.matcher import Matcher
from collections import Counter
# import nltk
# nltk.download('wordnet')
# from nltk.corpus import wordnet as wn
# from nltk.stem import WordNetLemmatizer

# lemmatizer = WordNetLemmatizer()

logger = logging.getLogger(__name__)
nlp = spacy.load('en_core_web_sm')

# not_applicable_items = ["food","eye","organ","brain","leg","hand","tongue","heart","skin","biscuit","diet","piece","mate","meal","shoulder","bit",
#                         "rock", "side","center","right","left","top","bottom","front","back","head","tail","foot","leg","arm","eye","ear","nose","mouth","teeth"
#                         ]

usual_food_items = [
    'cod', 'crabs', 'crustaceans', 'cuttlefish', 'dolphins', 'fish', 'herring', 'invertebrates', 
    'lobster', 'mackerel', 'marine birds', 'meat', 'octopus', 'polar bears', 'porpoises', 'sea lions', 
    'seals', 'sharks', 'shrimp', 'squid', 'whales', 'bamboo', 'bananas', 'bark', 'berries', 'branches', 
    'bushes', 'crops', 'flowers', 'fruit', 'grass', 'herbs', 'leaves', 'nuts', 'plants', 'roots', 'seed pods', 
    'shrubs', 'soil', 'sugarcane', 'twigs', 'vegetables', 'vegetation', 'apples', 'birds', 
    'carrots', 'eggs', 'fungi', 'honey', 'insects', 'rice gruel', 'rodents', 'shoots', 'small mammals', 
    'stems', 'sweet potatoes', 'wild tubers', 'yam', 'acacias', 'foliage', 'grain', 'vines', 
    'antelopes', 'buffaloes', 'crocodiles', 'deer', 'domestic cattle', 'flesh', 'gazelles', 
    'giraffes', 'hares', 'hippos', 'humans', 'lizards', 'mice', 'reptiles', 'rhinos', 'springbok', 
    'tortoises', 'wild hogs', 'wildebeests', 'young elephants', 'zebras', 'herbivore', 'carnivore',
    'omnivore', 'plant', 'insect', 'rodent', 'vertebrate', 'bison', 'bovine', 'cattle', 'chickens',
    'duck', 'goat', 'horse', 'lizard', 'pig', 'rabbit', 'sheep', 'turkey', 'wolf', 'bison','tree',
    'food', 'organ', 'brain', 'leg', 'hand', 'tongue', 'heart', 'skin', 'biscuit', 'diet', 'piece',
    'crustacean', 'fish', 'invertebrate', 'mammal', 'reptile', 'sheep', 'turtle', 'bird', 'cow',
    'shark', 'squid', 'whale', 'fish','small animal', 'large animal', 'bamboo shoot', 'banana',
    'bark', 'berry', 'branch', 'bush', 'crop', 'flower', 'fruit', 'grass', 'herb', 'leaf', 'nut'
]
# from transformers import pipeline

# model_name = "deepset/roberta-base-squad2"

# qa_roberta = pipeline('question-answering', model=model_name, tokenizer=model_name, device=0)


# def if_food(word):

#     syns = wn.synsets(str(word), pos = wn.NOUN)

#     for syn in syns:
#         if 'food' in syn.lexname():
#             return 1
#     return 0

# def get_all_food(text: str) -> List[str]:
#     """
#     Task: Extract all foods from the given text.
#     :param text: text
#     :return: list of foods
#     """
#     food = []
#     doc = nlp(text)
#     for token in doc:
#         if token.pos_ == 'NOUN':
#             if if_food(token.text) == 1:
#                 text = lemmatizer.lemmatize(token.text, pos = 'n')
#                 # if text not in not_applicable_items:
#                 food.append(text)
#     return food

# def line_preprocess(line: str) -> str:
#      line = line.lower()
#      # everything after eat or eats or consumed or eaten or eating or consumes or consume is food
#      try:
#          line = line.split("eat")[1]
#      except IndexError:
#         try:
#             line = line.split("eats")[1]
#         except IndexError:
#              try:
#                  line = line.split("ate")[1]
#              except IndexError:
#                  try:
#                      line = line.split("eaten")[1]
#                  except IndexError:
#                      try:
#                         line = line.split("eating")[1]
#                      except IndexError:
#                         try:
#                             line = line.split("consumed")[1]
#                         except IndexError:
#                             try:
#                                 line = line.split("consumes")[1]
#                             except IndexError:
#                                 try:
#                                     line = line.split("consume")[1]
#                                 except IndexError:
#                                     line = line
#      return line
                     
      
# def your_solution_v1(animal: str, doc_list: List[Dict[str, str]]) -> List[Tuple[str, int]]:
#     """
#     Task: Extract things that the given animal eats. These things should be mentioned in the given list of documents.
#     Each document in ``doc_list`` is a dictionary with keys ``animal``, ``url``, ``title`` and ``text``, whereas
#     ``text`` points to the content of the document.

#     :param animal: The animal to extract diets for.
#     :param doc_list: A list of retrived documents.
#     :return: A list of things that the animal eats along with their frequencies.
#     """

#     logger.info(f"Animal: \"{animal}\". Number of documents: {len(doc_list)}.")

#     # You can directly use the following list of documents, which is a list of str, if you don't need other information (i.e., url, title).
#     documents = [doc["text"] for doc in doc_list]
    
#     # TODO Implement your own method here for open information extraction.
#     # You must extract things that are explicitly mentioned in the documents.
#     # You cannot use any external CSK resources (e.g., ConceptNet, Quasimodo, Ascent, etc.).
    
#     foods = []
#     for each_line in documents:
#         # each_line = line_preprocess(each_line)
#         foods.extend(get_all_food(each_line))
    
#     food_list = Counter(foods)
#     result = food_list.most_common(30)
#     print(result)
#     # Output example:
#     return result

def your_solution(animal: str, doc_list: List[Dict[str, str]]) -> List[Tuple[str, int]]:
        matcher = Matcher(nlp.vocab)
        pattern1 = [
                {"LEMMA": "eat"},
                {"POS": "NOUN"},
            ]
        
        pattern2 = [
                {"LEMMA": "consume"},
                {"POS": "NOUN"},
            ]
        
        pattern3 = [
                {"LEMMA": "diet"},
                {"POS": "NOUN"},
            ]
        pattern4 = [
                {"LEMMA": "contain"},
                {"POS": "NOUN"},
            ]
        
        pattern5 = [
                {"LEMMA": "comprise"},
                {"POS": "NOUN"},
            ]
        
        pattern6 = [
                {"LEMMA": "consist"},
                {"POS": "NOUN"},
            ]
        pattern7 = [
                {"LEMMA": "hunt"},
                {"POS": "NOUN"},
            ]
            
        
        matcher.add("eatPattern", [pattern1, pattern2, pattern3, pattern4, pattern5,pattern6,pattern7])

        logger.info(
            f"Animal: \"{animal}\". Number of documents: {len(doc_list)}. Running SpaCy...")
        for doc in doc_list:
            doc["spacy_doc"] = nlp(doc["text"])

        matches = []
        for doc in doc_list:
            matches.append(matcher(doc["spacy_doc"]))

        diets = []
        for a, ms in zip(doc_list, matches):
            for m in ms:
                _, _, end = m
                diets.append(a["spacy_doc"][end-1].text.lower())

        # this is to make sure our animals are not eating plastic bottles :D
        for items in diets:
            
            if items not in usual_food_items:
                # print(items)
                diets.remove(items)
            else:
                continue
        result = Counter(diets).most_common()
        # print(result)
        return result

# def your_solution_v3(animal: str, doc_list: List[Dict[str, str]]) -> List[Tuple[str, int]]:
#     logger.info(f"Animal: \"{animal}\". Number of documents: {len(doc_list)}.")

#     # You can directly use the following list of documents, which is a list of str, if you don't need other information (i.e., url, title).
#     documents = [doc["text"] for doc in doc_list]
#     context = " ".join(documents)
#     QA_input = {
#     'question': 'What do f{animal} eat?'.format(animal=animal),
#     'context': context
#     }
    
#     QA_output = qa_roberta(QA_input)
    
#     foods = text_process(QA_output['answer'])
#     food_list = Counter(foods)
#     result = food_list.most_common(30)
#     # Output example:
#     return result
    

# def text_process(QA_output: str) -> List[str]:
#     QA_output = QA_output.replace("and", ",")
#     QA_output = QA_output.replace(",", " ")
#     list_of_food = QA_output.split(" ")
#     return list_of_food
    