
# Lab04 - submission

Everything you need to know about my submission.
```
Name: Shantanu Kumar Rahut
Matriculation Number: 7015438

```

## Helper functions I wrote in run.py

#### load_data(path: str)


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `path` | `string` | **Required**. Path to webisalod-pairs.txt |

```returns pandas dataframe```
#### data_preprocessing(df: pd.DataFrame)

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `df`      | `pandas dataframe` | **Required**. Dataframe to pre-process |

``` returns processed dataframe ```
#### create_dictionary(df: pd.DataFrame)

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `df` | `pandas dataframe` | **Required**. Creates dictionary from dataframe |

``` returns dictionary ```
#### save_to_json(dictionary: dict, path: str)

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `dictionary` | `dict` | **Required**. Dictionary that we want to save as json |
| `path` | `str` | **Required**. Json file path |

``` returns None ```
#### load_json_to_dictionary(path: str)

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `path` | `str` | **Required**. Json file path |

``` returns dictionary ```


***This function below calls all previous functions mentioned.***
#### from_webisalod_to_dict_json():

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
|  |  |    |

```returns None```



***This function calls all previously mentioned functions.***

***and then plots the graph.***
#### main(input_file: str)

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `input_file` | `str` | **Required**. Input file path |

``` returns None ```
## Environment and other information

To run this , you **might** need following Environment

`Operating System: Windows 10`

`Python 3.9.6`

### Packages you might need
```
from matplotlib.pyplot import subplot
import pandas as pd
import matplotlib.pyplot as plt
import json
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import sys
```
Download anything that you don't have already. And you can also find
**requirements.txt** file to help you with installing packages.

