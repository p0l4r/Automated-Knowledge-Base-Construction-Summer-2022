"""
Author: Tuan-Phong Nguyen
Date: 2022-06-03
"""

import argparse
import json
import logging
import os
from multiprocessing import Pool
from pathlib import Path

from baseline import simple_pattern_search
from evaluate import evaluate_predictions
from file_io import (read_animal_file, read_document_file,
                     read_ground_truth_file)
from solution import your_solution

logging.basicConfig(level=logging.INFO,
                    format='[%(processName)s] [%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                    datefmt='%d-%m %H:%M:%S')

logger = logging.getLogger(__name__)

CUR_DIR = Path(os.path.dirname(os.path.abspath(__file__)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_file", type=str,
                        default=str(CUR_DIR / "public_predictions.json"))
    parser.add_argument("--data_dir", type=str,
                        default=str(CUR_DIR / "public_test"))
    parser.add_argument("--k", type=int, default=30)
    parser.add_argument("--test_animals", type=str, default="all")
    parser.add_argument("--run_baseline", action="store_true")
    parser.add_argument("--n_processes", type=int, default=1)
    args = parser.parse_args()

    # Checking the command line arguments
    data_dir = Path(args.data_dir)
    assert data_dir.exists(), "data_dir must exist"
    assert data_dir.is_dir(), "data_dir must be a directory"

    logger.info(f"Select data directory: \"{data_dir}\"")

    doc_dir = data_dir / "documents"
    assert doc_dir.exists(), f"{doc_dir} must exist"
    assert doc_dir.is_dir(), f"{doc_dir} must be a directory"

    animal_fp = data_dir / "animals.txt"
    assert animal_fp.exists(), f"{animal_fp} must exist"

    labels_fp = data_dir / "labels.json"

    assert 0 < args.k <= 30, "k must be in [1, 30]"

    # Read data
    animals = read_animal_file(animal_fp)
    if args.test_animals.lower() != "all":
        valid_animals = set(animals)
        animals = []
        for animal in args.test_animals.lower().split(","):
            if animal in valid_animals:
                animals.append(animal.strip())

    doc_file_paths = [
        doc_dir / f"{animal.replace(' ', '_')}.jsonl.gz" for animal in animals]
    doc_lists = [read_document_file(doc_file_path)
                 for doc_file_path in doc_file_paths]

    # Predict
    func = your_solution
    if args.run_baseline:
        func = simple_pattern_search
    logger.info(
        f"Running the extraction function ({func.__name__}) for {len(animals)} animals: {json.dumps(animals)}.")

    n_processes = min(args.n_processes, len(animals))
    logger.info(f"Number of processes: {n_processes}")
    if n_processes > 1:  # multiprocessing (faster)
        with Pool(processes=n_processes) as pool:
            diet_lists = pool.starmap(func, zip(animals, doc_lists))
    else:  # sequential (slower)
        diet_lists = [func(animal=animal, doc_list=doc_list) for animal, doc_list in
                      zip(animals, doc_lists)]

    predictions = {animal: [d[0] for d in sorted(diet_list, key=lambda x: x[1], reverse=True)]
                   for animal, diet_list in zip(animals, diet_lists)}

    # Write predictions
    with open(args.out_file, "w+") as f:
        json.dump(predictions, f, indent=4)

    # Evaluate
    if labels_fp.exists():
        return evaluate_predictions(
            read_ground_truth_file(labels_fp), predictions, args.k)


if __name__ == "__main__":
    main()
