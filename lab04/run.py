from matplotlib.pyplot import subplot
import pandas as pd
import matplotlib.pyplot as plt
import json
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import sys

def load_data(path: str)-> pd.DataFrame:
    """
    Loads data from a csv file.
    Properly.
    """
    # Read in the data
    df = pd.read_csv(path, sep='\t', header= None)
    df.columns = ["word","cs"]

    df['hyponym'] = df['word'].str.split(';').str[0]
    df['hypernym'] = df['word'].str.split(';').str[1]

    df.drop(columns=['word'], inplace=True)

    df["confidence_score"]= df["cs"]

    df.drop(columns=['cs'], inplace=True)

    return df

def data_preprocessing(df: pd.DataFrame)-> pd.DataFrame:
    """
    Pre processes the data.
    """
    # Drop rows with NaN values
    df.dropna(inplace=True)
    # Drop rows with confidence score of 0.70
    df = df[df['confidence_score'] > 0.69]
    # drop rows with specific hyponym and hypernym
    df = df[df['hyponym'] != ' _name_']
    df = df[df['hyponym'] != ' _thing_']
    df = df[df['hypernym'] != ' _name_']
    df = df[df['hypernym'] != ' _thing_']
    # remove punctuation, numbers, and special characters
    df['hyponym'] = df['hyponym'].str.replace('[_]', ' ', regex=True)
    df['hypernym'] = df['hypernym'].str.replace('[_]', ' ', regex=True)
    df['hyponym'] = df['hyponym'].str.replace('[^a-zA-Z0-9\s]', '', regex=True)
    df['hypernym'] = df['hypernym'].str.replace('[^a-zA-Z0-9\s]', '', regex=True)
    df = df.applymap(lambda x: x.strip() if type(x) == str else x)
    return df

def create_dictionary(df: pd.DataFrame)-> dict:
    """
    Creates a dictionary of the data.
    """
    # create a dictionary of the data
    dictionary = {}
    for index, row in df.iterrows():
        try:
            dictionary[row['hyponym']].append(row['hypernym'])
            dictionary[row['hypernym']].append(row['hyponym'])
        except KeyError:
            dictionary[row['hyponym']] = [row['hypernym']]
            dictionary[row['hypernym']] = [row['hyponym']]
    return dictionary


def save_to_json(dictionary: dict, path: str)-> None:
    """
    Saves the dictionary to a json file.
    """
    with open(path, 'w') as f:
        json.dump(dictionary, f)

def load_json_to_dictionary(path: str)-> dict:
    """
    Loads a json file to a dictionary.
    """
    with open(path, 'r') as f:
        dictionary = json.load(f)
    return dictionary

def from_webisalod_to_dict_json():
    '''
    This function creates a dictionary.json file from the data in webisalod-pairs.txt.
    
    The dictionary.json file is then used to create the graph.
    '''
    df = load_data("webisalod-pairs.txt")
    df = data_preprocessing(df)
    dictionary = create_dictionary(df)
    save_to_json(dictionary, "dictionary.json")
    print("Dictionary saved to dictionary.json")
    
def main(input_file: str)-> None:
    # To create the dictionary from webisalod-pairs.txt , just uncomment the line below.
    try:
        from_webisalod_to_dict_json() ## run this if you want to create the dictionary.json file.
    except FileNotFoundError:
        print("Maybe you don't have webisalod-pairs.txt in the same directory as this file.")
        print("Don't worry, I have saved everything needed from the file to dictionary.json for you.")
        pass
    
    # I created dictionary.json from the data in webisalod-pairs.txt
    loaded_dict = load_json_to_dictionary('dictionary.json') ## load the dictionary.json file.
    
    # Loads data from input files i.e. input-1.txt, input-2.txt, input-3.txt
    data = open(input_file, 'r').readlines()
    data = [line.strip() for line in data]

    
    # create entity-relationship graph
    draft_graph = {}
    for i in data:
        for key, value in loaded_dict.items():
            if i in key:
                if key not in draft_graph:
                    draft_graph[key] = value
    
    graph = {}
    for i in data:
        try:
            graph[i] = draft_graph[i]
        except KeyError:
            pass
    
    # create a networkx graph
    G = nx.Graph()
    G.add_node("entity")
    for key, value in graph.items():
        G.add_node(key)
        for v in value:
            G.add_edge("entity", key)
            G.add_edge(key, v)
            
    # draw the graph
    pos = graphviz_layout(G, prog='fdp')
    nx.draw(G, with_labels=True, pos= pos, ax=subplot(111))
    plt.show()
    
    
            
    

if __name__ == '__main__':
        if len(sys.argv) != 2:
            raise ValueError('Expected exactly 1 argument: input file ')
        main(sys.argv[1])

 