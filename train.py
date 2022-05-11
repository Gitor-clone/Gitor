# using node2vec to calculate the similarity between nodes
import argparse
import os
import networkx as nx
# from node2vec import Node2Vec
from nodevectors import Node2Vec
from nodevectors import ProNE
import extract
import side_info
import time
import psutil
from concurrent.futures import ProcessPoolExecutor, as_completed

parser = argparse.ArgumentParser()

parser.add_argument('--embed_dim', type=int, default=16)
parser.add_argument('--save_path', default='./time_exp/both_16/')
parser.add_argument('--source_func_path', default='./data/id2sourcecode/')

args = parser.parse_args()

# if the save path does not exist, create the directory
if not os.path.exists(args.save_path):
    os.makedirs(args.save_path)

print('INFO: --------args----------')
for k in list(vars(args).keys()):
    print('INFO: %s: %s' % (k, vars(args)[k]))
print('INFO: --------args----------\n')

# keywords 
# graph = extract.build_graph(extract.KEYWORDS)
# extract.add_nodes(graph, args.source_func_path)
begin_time = time.time()
# # side info
graph1 = side_info.build_graph(side_info.side_keywords)
graph2 = side_info.build_graph(side_info.side_keywords)

executor = ProcessPoolExecutor(max_workers=11)
task_list = [
    executor.submit(side_info.add_nodes, graph1, args.source_func_path),
    executor.submit(side_info.add_nodes, graph2, args.source_func_path)
]
process_results = [task.result() for task in as_completed(task_list)]

graph = nx.compose(graph1,graph2)
# side_info.add_nodes(graph, args.source_func_path)


# # both
# graph = extract.build_graph(list(set(extract.KEYWORDS)|set(side_info.side_keywords)))
# extract.add_nodes(graph, args.source_func_path)
# side_info.add_nodes(graph, args.source_func_path)


# # Precompute probabilities and generate walks - **ON WINDOWS ONLY WORKS WITH workers=1**
# node2vec = Node2Vec(graph, dimensions=args.embed_dim, walk_length=30, num_walks=200, workers=48)  # Use temp_folder for big graphs

# g2v = Node2Vec(
#     n_components=args.embed_dim,
#     walklen=10
# )

print(u'mem is: %.4f GB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024) )

g2v = ProNE(
    n_components=args.embed_dim
)

# Embed nodes
# model = node2vec.fit(window=10, min_count=1, batch_words=4, workers=48)  # Any keywords acceptable by gensim.Word2Vec can be passed, `dimensions` and `workers` are automatically passed (from the Node2Vec constructor)
# g2v.fit(graph)

print(f'\n\nINFO: all time is {time.time() - begin_time}')

# g2v.save(os.path.join(args.save_path, "embedding"))
