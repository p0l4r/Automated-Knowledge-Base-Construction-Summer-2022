"""
Author: Tuan-Phong Nguyen
Date: 2022-06-03
"""

import logging
from collections import Counter
from typing import Dict, List, Tuple

import spacy
from spacy.matcher import Matcher

logger = logging.getLogger(__name__)

nlp = spacy.load("en_core_web_sm")


def simple_pattern_search(animal: str, doc_list: List[Dict[str, str]]) -> List[Tuple[str, int]]:
    """
    This approach uses a simple pattern search to find what the animal eats in the articles.
    First, it finds the occurences of the pattern "<animal>s* [eat|eats|ate|eaten|eating] <POS:NOUN>".
    Then, it extracts the noun as result.

    References:
      - SpaCy's rule-based matching: https://spacy.io/usage/rule-based-matching
      - Demo: https://explosion.ai/demos/matcher
    """

    matcher = Matcher(nlp.vocab)
    pattern = [
        {"LOWER": {"IN": [f"{animal}", f"{animal}s"]}},
        {"LEMMA": "eat"},
        {"POS": "NOUN"},
    ]
    matcher.add("eatPattern", [pattern])

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

    return Counter(diets).most_common()
