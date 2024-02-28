# extract all java keywords from java source code files and build a keywords graph using networkx
import os
import re
import io
from tkinter import E
import networkx as nx
# import matplotlib.pyplot as plt
from javalang import tokenizer

# class Keyword(JavaToken):
# KEYWORDS = set(['abstract', 'assert', 'boolean', 'break', 'byte', 'case',
#                 'catch', 'char', 'class', 'const', 'continue', 'default',
#                 'do', 'double', 'else', 'enum', 'extends', 'exports', 'final',
#                 'finally', 'float', 'for', 'goto', 'if', 'implements',
#                 'import', 'instanceof', 'int', 'interface', 'long', 'native',
#                 'new', 'package', 'private', 'protected', 'public', 'requires', 'return',
#                 'short', 'static', 'strictfp', 'super', 'switch',
#                 'synchronized', 'this', 'throw', 'throws', 'transient', 'try', 'var',
#                 'void', 'volatile', 'while'])

KEYWORDS = set(['abstract', 'assert', 'boolean', 'break', 'byte', 'case',
                'catch', 'char', 'class', 'const', 'continue', 'default',
                'do', 'double', 'else', 'enum', 'extends', 'final',
                'finally', 'float', 'for', 'goto', 'if', 'implements',
                'import', 'instanceof', 'int', 'interface', 'long', 'native',
                'new', 'package', 'private', 'protected', 'public', 'return',
                'short', 'static', 'strictfp', 'super', 'switch',
                'synchronized', 'this', 'throw', 'throws', 'transient', 'try',
                'void', 'volatile', 'while'])

# use javalang to extract keywords defined above
def extract_keywords(file_path):
    file = io.open(file_path, 'r', encoding='utf-8')
    try:
        tokens = list(tokenizer.tokenize(file.read()))
    except:
        with open('./failed.txt', 'a+') as failed_file:
            failed_file.write(file_path + '\n')
            failed_file.close()
            return
    keywords = []
    for line in tokens:
        if line.value in KEYWORDS:
            keywords.append(line.value)
    # convert the list to dict, so that the value of each keyword is the frequency of the keyword
    keywords_dict = {}
    for keyword in keywords:
        if keyword in keywords_dict:
            keywords_dict[keyword] += 1
        else:
            keywords_dict[keyword] = 1
    return keywords_dict

# build a graph using networkx
def build_graph(keywords):
    G = nx.DiGraph()
    for keyword in keywords:
        G.add_node(keyword)
    return G

# # draw the graph
# def draw_graph(G):
#     pos = nx.spring_layout(G)
#     nx.draw(G, pos, with_labels=True)
#     plt.show()

# # for each file in the directory, add a node on the graph
# def add_nodes(G, dir_path):
#     for file in os.listdir(dir_path):
#         file_path = os.path.join(dir_path, file)
#         if os.path.isfile(file_path):
#             keywords = extract_keywords(file_path)
#             if keywords:
#                 G.add_node(file)
#                 # G.add_nodes_from(keywords)
#                 for keyword in keywords:
#                     G.add_edge(file, keyword)

# for each file in the directory, add a node on the graph and set the weight to frequency of the keyword
def add_nodes(G, dir_path):
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        if os.path.isfile(file_path):
            G.add_node(file)
            keywords_dict= extract_keywords(file_path)
            if keywords_dict:
                for keyword in keywords_dict:
                    G.add_edge(file, keyword, weight=keywords_dict[keyword]) # weight is the frequency of the keyword