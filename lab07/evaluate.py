"""
Author: Tuan-Phong Nguyen
Date: 2022-06-03
"""

import argparse
import logging
from typing import List

import spacy

from file_io import read_ground_truth_file

logger = logging.getLogger(__name__)

nlp = spacy.load("en_core_web_sm")


def get_head_word(phrase: str) -> str:
    """
    Gets head word of a phrase.
    :param phrase: phrase
    :return: head word of a phrase
    """
    if phrase.strip() == "":
        return ""

    try:
        # try to get head word using SpaCy
        return list(nlp(phrase.lower().strip()).sents)[0].root.lemma_
    except Exception:
        # if error occurs, return the last word of the phrase
        return phrase.lower().strip().split()[-1]


def normalize_object_phrase_list(phrase_list: List[str]) -> List[str]:
    """
    Normalizes object phrase list.
    :param phrase_list: list of object phrases
    :return: normalized object phrase list (i.e., list of head words)
    """
    seen = set()
    normalized_phrase_list = []
    for phrase in phrase_list:
        head_word = get_head_word(phrase)
        if head_word in seen:
            continue
        seen.add(head_word)
        normalized_phrase_list.append(head_word)
    return normalized_phrase_list


def precision_at_k(tgt_list, pred_list, k):
    """
    Calculates precision at k.
    :param tgt_list: list of target object phrases
    :param pred_list: list of predicted object phrases
    :param k: number of predicted object phrases to consider
    :return: precision at k
    """
    tp = 0
    for pred in pred_list[:k]:
        if pred in tgt_list:
            tp += 1
    try:
        return tp / len(pred_list[:k])
    except ZeroDivisionError:
        return 0.0


def recall_at_k(tgt_list, pred_list, k):
    """
    Calculates recall at k.
    :param tgt_list: list of target object phrases
    :param pred_list: list of predicted object phrases
    :param k: number of predicted object phrases to consider
    :return: recall at k
    """
    tp = 0
    for tgt in tgt_list:
        if tgt in pred_list[:k]:
            tp += 1
    try:
        return tp / len(tgt_list)
    except ZeroDivisionError:
        return 0.0


def f1(p, r):
    """
    Calculates F1 score.
    :param p: precision
    :param r: recall
    :return: F1 score
    """
    try:
        return 2 * p * r / (p + r)
    except ZeroDivisionError:
        return 0.0


def f1_at_k(tgt_list, pred_list, k):
    """
    Calculates F1 at k.
    :param tgt_list: list of target object phrases
    :param pred_list: list of predicted object phrases
    :param k: number of predicted object phrases to consider
    :return: F1 at k
    """
    p = precision_at_k(tgt_list, pred_list, k)
    r = recall_at_k(tgt_list, pred_list, k)
    return f1(p, r)


def true_positive(tgt_list, pred_list, k):
    """
    Calculates true positive.
    :param tgt_list: list of target object phrases
    :param pred_list: list of predicted object phrases
    :param k: number of predicted object phrases to consider
    :return: true positive
    """
    tp = 0
    for pred in pred_list[:k]:
        if pred in tgt_list:
            tp += 1
    return tp


def compute_micro_avg(results):
    """
    Computes micro-average.
    :param results: list of results
    :return: micro-average
    """
    TP_key = list(k for k in results[0].keys() if k.startswith("TP@"))[0]
    TP = sum(result[TP_key] for result in results)
    PSize = sum(result["PSize"] for result in results)
    TSize = sum(result["TSize"] for result in results)
    try:
        micro_p = TP / PSize
    except ZeroDivisionError:
        micro_p = 0.0
    try:
        micro_r = TP / TSize
    except ZeroDivisionError:
        micro_r = 0.0
    try:
        micro_f1 = 2 * micro_p * micro_r / (micro_p + micro_r)
    except ZeroDivisionError:
        micro_f1 = 0.0

    return micro_p, micro_r, micro_f1


def compute_macro_avg(results):
    """
    Computes macro-average.
    :param results: list of results
    :return: macro-average
    """
    P_key = list(k for k in results[0].keys() if k.startswith("P@"))[0]
    R_key = list(k for k in results[0].keys() if k.startswith("R@"))[0]

    macro_p = sum(result[P_key] for result in results) / len(results)
    macro_r = sum(result[R_key] for result in results) / len(results)

    try:
        macro_f1 = 2 * macro_p * macro_r / (macro_p + macro_r)
    except ZeroDivisionError:
        macro_f1 = 0.0

    return macro_p, macro_r, macro_f1


def print_table_rule(row_format, field_names, sep="-"):
    """
    Prints table rule.
    :param row_format: row format
    :param field_names: field names
    :param sep: separator
    :return: None
    """
    print(row_format.format(
        *([sep * 15] + [sep * 8] * (len(field_names) - 1))))


def print_table_evaluation_results(results):
    """
    Prints evaluation results in a table.
    :param results: list of evaluation results
    :return: None
    """
    field_names = list(k for k in results[0].keys() if k == "Animal" or k.startswith(
        "P@") or k.startswith("R@") or k.startswith("F1@"))

    rule_format = "+{:<15}+" + "{:<8}+" * (len(field_names) - 1)
    row_format = "|{:<15}|" + "{:<8}|" * (len(field_names) - 1)

    print_table_rule(rule_format, field_names, sep="-")

    print(row_format.format(*[" " + field for field in field_names]))

    print_table_rule(rule_format, field_names, sep="=")

    for result in results:
        print(row_format.format(*[" " + (str(value) if not isinstance(value,
              float) else "%.3f" % value) for value in result.values()]))

    # compute micro average
    micro_p, micro_r, micro_f1 = compute_micro_avg(results)
    print_table_rule(rule_format, field_names, sep="=")
    print(row_format.format(*[" Micro avg.", " %.3f" %
          micro_p, " %.3f" % micro_r, " %.3f" % micro_f1]))

    # compute macro average
    macro_p, macro_r, macro_f1 = compute_macro_avg(results)
    print_table_rule(rule_format, field_names, sep="=")

    print(row_format.format(*[" Macro avg.", " %.3f" %
          macro_p, " %.3f" % macro_r, " %.3f" % macro_f1]))

    print_table_rule(rule_format, field_names, sep="-")


def evaluate_predictions(tgt_animals_diets, pred_animals_diets, k, print_results=True):
    """
    Evaluates predictions.
    :param tgt_animals_diets: list of target animals and diets
    :param pred_animals_diets: list of predicted animals and diets
    :param k: number of predicted diets to consider
    :return: evaluation results
    """
    logger.info(
        f"Evaluating {len(tgt_animals_diets)} animals: {', '.join(tgt_animals_diets.keys())}")

    results = []
    for animal, tgt_diets in tgt_animals_diets.items():
        tgt_diets = normalize_object_phrase_list(tgt_diets)

        try:
            pred_diets = pred_animals_diets[animal]
        except KeyError:
            pred_diets = []
            logger.warn(f"\"{animal}\" is not in the prediction list.")

        pred_diets = normalize_object_phrase_list(pred_diets)

        p = precision_at_k(tgt_diets, pred_diets, k)
        r = recall_at_k(tgt_diets, pred_diets, k)
        f = f1(p, r)

        TP = true_positive(tgt_diets, pred_diets, k)
        pred_size = len(pred_diets[:k])
        tgt_size = len(tgt_diets)

        results.append({
            "Animal": animal,
            f"P@{k}": p,
            f"R@{k}": r,
            f"F1@{k}": f,
            f"TP@{k}": TP,
            f"PSize": pred_size,
            f"TSize": tgt_size,
        })

    if print_results:
        print("Evaluation results:")
        print_table_evaluation_results(results)

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tgt_file", type=str, required=True)
    parser.add_argument("--pred_file", type=str, required=True)
    parser.add_argument("--k", type=int, default=30)
    args = parser.parse_args()

    assert 0 < args.k <= 30, "k must be in [1, 30]"
    k = args.k

    tgt_animals_diets = read_ground_truth_file(args.tgt_file)
    pred_animals_diets = read_ground_truth_file(args.pred_file)

    return evaluate_predictions(tgt_animals_diets, pred_animals_diets, k)


if __name__ == "__main__":
    main()
