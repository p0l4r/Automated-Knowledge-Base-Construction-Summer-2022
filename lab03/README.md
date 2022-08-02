
# Lab03 - submission

Everything you need to know about my submission.
```
Name: Shantanu Kumar Rahut
Matriculation Number: 7015438

```

## Helper functions I wrote in run.py

#### process_sentence(sent: str)


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `sent` | `string` | **Required**. The sentence to process |

```returns processed sentence```
#### what_is_your_entity_type(sent: str,entity: str)

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `sent`      | `string` | **Required**. Sentence from the dataframe row |
| `entity`      | `string` | **Required**. Entity from the dataframe row |

``` returns entity type aka entity info of a sentence ```
#### trying_out_some_more_rules(entity_info:str)

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `entity_info` | `string` | **Required**. Predicted entity_info or entity type |

``` returns further processed entity info ```

## Environment and other information

To run this , you **might** need following Environment

`Operating System: Windows 10`

`Python 3.9.6`

### Packages you might need
```
import sys
import pandas as pd
import os
import nltk
import csv
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
```
Download anything that you don't have already. And you can also find
**requirements.txt** file to help you with installing packages.

