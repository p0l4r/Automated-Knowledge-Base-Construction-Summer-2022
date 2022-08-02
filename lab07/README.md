# Lab 7: Commonsense Knowledge (AKBC22 @ UdS)

This repository contains code and data for Lab 7 of the 
[AKBC course](https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/teaching/ss2022/akbc) 
at
Saarland University in the Summer semester 2022.

You can start working on the assignment by following the getting-started steps.
If you encounter any technical problems or have any questions, first check out
the FAQs section below. If it couldn't answer your questions, use the Google
group to ask.

## Getting started

To get started, follow these steps:

1. Read the problem description in the
[assignment sheet](https://www.mpi-inf.mpg.de/fileadmin/inf/d5/teaching/ss22_akbc/lab07.pdf)
carefully.
2. Clone this repo:
```bash
$ git clone https://github.com/phongnt570/akbc22-lab07.git
$ cd akbc22-lab07
```
3. (Optional) Create a virtual Python environment (e.g., using 
[``venv``](https://docs.python.org/3/library/venv.html) or 
[``conda``](https://www.anaconda.com/)).
Then, activate the virtual environment whenever you start working on the
assignment.
4. If you haven't installed SpaCy:
```bash
$ pip3 install spacy
$ python3 -m spacy download en_core_web_sm
```
5. (Optional) Take a look at [``baseline.py``](baseline.py) for the tutor's
baseline algorithm, and try running it using this 
[guideline](#what-is-in-the-baselinepy-file).
6. Write your solution in the ``your_solution`` function in the 
[``solution.py``](solution.py) file.
7. Execute [``main.py``](main.py) to run your extraction algorithm and see the
evaluation results _on the public test_:
```bash
$ python3 main.py
```

## FAQs

### Where is my prediction output?

The default prediction file is ``public_predictions.json``. You can change that
using the ``--out_file`` argument:
```bash
$ python3 main.py --out_file /path/to/your/predictions_file.json
```

### Which animals are included in the public test data?

- The animals in the public test data are listed in
[``public_test/animals.txt``](public_test/animals.txt). 
- The retrieved documents for those animals can be found in
[``public_test/documents``](public_test/documents).
- The ground truth for the public test data can be found in
[``public_test/labels.json``](public_test/labels.json).

Functions in [``file_io.py``](file_io.py) handle reading these files.

### Running all animals is so slow, can I test my algorithm with fewer animals?

You can use the ``--test_animals`` argument to specify the animal(s) you want to
test, separated by commas:
```bash
$ python3 main.py --test_animals "elephant,giant panda"
```

### Running all animals is so slow, how could I speed it up?

You could use the ``--n_processes`` argument to run your extraction function
parallelly (each process runs the extraction function for one animal):
```bash
$ python3 main.py --n_processes 5
```

### What is in the [``baseline.py``](baseline.py) file?

This file contains the implementation of a simple baseline for this task.
You can run the baseline algorithm using the ``--run_baseline`` argument:
```bash
$ python3 main.py --run_baseline --n_processes 5
```

The evaluation results of the baseline algorithm can be seen in the following
table (tested on MacOS with Python 3.9.12, SpaCy 3.3.0).

| Animal        | P@30   | R@30   | F1@30  |
|---------------|-------:|-------:|-------:|
| dolphin       | 1.000  | 0.238  | 0.385  |
| elephant      | 0.286  | 0.091  | 0.138  |
| giant panda   | 0.000  | 0.000  | 0.000  |
| giraffe       | 0.333  | 0.133  | 0.190  |
| lion          | 0.364  | 0.160  | 0.222  |
| **Micro avg.**    | **0.448**  | **0.121**  | **0.191**  |
| **Macro avg.**    | **0.397**  | **0.124**  | **0.189**  |

### What is in the [``evaluate.py``](evaluate.py) file?

This file contains the code for evaluating your predictions, on the following
metrics: 
- Precision@k
- Recall@k 
- F1@k 

whereas k is default to 30 (the maximal
number of labels for an animal in the private test data).

We use head-word matching to identify correct answers.
