# side info
# 1. the max depth of the {} in the java source code
# 2. the num of {} in the main function
# 3. the num of container <> in the source code
# 4. the num of for and while loop in the main function
# 5. the num of if and switch in the main function

from itertools import count

from matplotlib.pyplot import draw, flag
from numpy import place
import extract
import io
import os
import networkx as nx
from javalang import tokenizer
import matplotlib.pyplot as plt

side_keywords = ['m_depth', 'p_num', 'for-while', 'if-switch']

# tokenize the java source code
def tokenize(file_path):
    file = io.open(file_path, 'r', encoding='utf-8')
    try:
        tokens = list(tokenizer.tokenize(file.read()))
    except:
        with open('./failed.txt', 'a+') as failed_file:
            failed_file.write(file_path + '\n')
            failed_file.close()
            return
    return tokens

# calculate the max depth of the {} in the java source code
def max_depth(tokens):
    max = 0
    depth = 0
    for line in tokens:
        if line.value == '{':
            depth += 1
        elif line.value == '}':
            max = max if max > depth else depth
            depth -= 1
    return max

# calculate the num of parallel {} in the function
def parallel_num(tokens):
    parallel_num = 1
    depth = 0
    for line in tokens:
        if line.value == '{':
            depth += 1
        elif line.value == '}':
            depth -= 1
            if depth == 1:
                parallel_num += 1
    return parallel_num

# calculate the num of for and while loop in the main function
def loop_num(tokens):
    loop_num = 0
    for line in tokens:
        if line.value == 'for':
            loop_num += 1
        elif line.value == 'while':
            loop_num += 1
    return loop_num

# calculate the num of if and switch in the main function
def if_num(tokens):
    if_num = 0
    for line in tokens:
        if line.value == 'if':
            if_num += 1
        elif line.value == 'case':
            if_num += 1
    return if_num

# count the number of numerical declarations in the source code
def num_declaration(tokens):
    num_declaration = 0
    for line in tokens:
        if line.value == 'int' or line.value == 'double' or line.value == 'float' or line.value == 'long' or line.value == 'short' or line.value == 'byte':
            num_declaration += 1
    return num_declaration

def build_graph(keywords):
    G = nx.DiGraph()
    for keyword in keywords:
        G.add_node(keyword)
    return G

def add_nodes(G, dir_path):
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        if os.path.isfile(file_path):
            tokens = tokenize(file_path)
            if tokens:
                depth = max_depth(tokens)
                G.add_edge(file, 'm_depth', weight = depth)
                if parallel_num(tokens):
                    G.add_edge(file, 'p_num', weight = parallel_num(tokens))
                if loop_num(tokens):
                    G.add_edge(file, 'for-while', weight = loop_num(tokens))
                if if_num(tokens):
                    G.add_edge(file, 'if-switch', weight = if_num(tokens))
                if num_declaration(tokens):
                    G.add_edge(file, 'num_declaration', weight = num_declaration(tokens))
