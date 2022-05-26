# Gitor: Scalable Code Clone Detection by Building Global Sample Graph

We propose Gitor to capture the underlying connections (\ie global information) among different code samples. Specifically, given a source code database, we first tokenize all code samples to extract the pre-defined global information (\eg keywords). After obtaining all samples' global information, we leverage them to build a large global sample graph where each node is a code sample or a type of global information. Then we apply a node embedding technique on the global sample graph to extract all samples' vector representations. After collecting all code samples' vectors, we can simply compare the similarity between any two samples to detect possible clone pairs. More importantly, since the obtained vector of a sample is from a global sample graph, we can combine it with its own code features to improve the code clone detection performance. To demonstrate the effectiveness of Gitor, we evaluate it on a widely used dataset namely BigCloneBench. Our experimental results show that Gitor has higher accuracy in terms of code clone detection and excellent execution time for inputs of various sizes (1–100 MLOC) compared to existing state-of-the-art tools. Moreover, we also evaluate the combination of Gitor with other traditional vector-based clone detection methods, the results show that the use of Gitor enables them detect more code clones with higher F1.

This repository contains the source code of Gitor, which can be used to reproduce our results.

extract.py: Used to extract global information (Keywords) from code samples.\
side_info.py: Used to extract side information from code samples.\
train.py: Used for node embedding.\
detect.py: Used for code clone detection.\