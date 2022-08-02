"""
Author: Tuan-Phong Nguyen
Date: 2022-06-03
"""

import gzip
import json
from typing import Dict, List


def read_animal_file(file_path) -> List[str]:
    with open(file_path, "r") as f:
        return [line.strip().lower() for line in f.readlines() if line.strip()]


def read_document_file(file_path) -> List[Dict[str, str]]:
    # with open(file_path, "r") as f:
    #     return [json.loads(line) for line in f.readlines()]
    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def read_ground_truth_file(file_path) -> Dict[str, List[str]]:
    with open(file_path, "r") as f:
        return json.load(f)
