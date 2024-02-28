# Gitor

We propose *Gitor* to capture the underlying connections (i.e., *global information*) among different code samples. Specifically, given a source code database, we first tokenize all code samples to extract the pre-defined *global information* (e.g., *keywords*). After obtaining all samples' global information, we leverage them to build a large *global sample graph* where each node is a code sample or a type of global information. Then we apply a node embedding technique on the global sample graph to extract all samples' vector representations. After collecting all code samples' vectors, we can simply compare the similarity between any two samples to detect possible clone pairs. More importantly, since the obtained vector of a sample is from a global sample graph, we can combine it with its code features to improve the code clone detection performance.

The Gitor mainly consists of four phases:

- `extract.py`: Used to extract global information (Keywords) from code samples.
- `side_info.py`: Used to extract side information from code samples.
- `train.py`: Used for node embedding.
- `detect.py`: Used for code clone detection.

This is the README.md file for the code of the paper:

Shan, J., Dou, S., Wu, Y., Wu, H., & Liu, Y. (2023). Gitor: Scalable Code Clone Detection by Building Global Sample Graph. In *Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering* (pp. 784–795). https://doi.org/10.1145/3611643.3616371

Abstract: Code clone detection is about finding out similar code fragments, which has drawn much attention in software engineering since it is important for software maintenance and evolution. Researchers have proposed many techniques and tools for source code clone detection, but current detection methods concentrate on analyzing or processing code samples individually without exploring the underlying connections among code samples. In this paper, we propose Gitor to capture the underlying connections among different code samples. Specifically, given a source code database, we first tokenize all code samples to extract the pre-defined individual information (keywords). After obtaining all samples’ individual information, we leverage them to build a large global sample graph where each node is a code sample or a type of individual information. Then we apply a node embedding technique on the global sample graph to extract all the samples’ vector representations. After collecting all code samples’ vectors, we can simply compare the similarity between any two samples to detect possible clone pairs. More importantly, since the obtained vector of a sample is from a global sample graph, we can combine it with its own code features to improve the code clone detection performance. To demonstrate the effectiveness of Gitor, we evaluate it on a widely used dataset namely BigCloneBench. Our experimental results show that Gitor has higher accuracy in terms of code clone detection and excellent execution time for inputs of various sizes (1–100 MLOC) compared to existing state-of-the-art tools. Moreover, we also evaluate the combination of Gitor with other traditional vector-based clone detection methods, the results show that the use of Gitor enables them detect more code clones with higher F1.

We welcome citations of our paper. If you find Gitor useful for your research, please consider citing it using the following Bibtex entry:

```
@inproceedings{10.1145/3611643.3616371,
author = {Shan, Junjie and Dou, Shihan and Wu, Yueming and Wu, Hairu and Liu, Yang},
title = {Gitor: Scalable Code Clone Detection by Building Global Sample Graph},
year = {2023},
isbn = {9798400703270},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3611643.3616371},
doi = {10.1145/3611643.3616371},
booktitle = {Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering},
pages = {784–795},
numpages = {12},
keywords = {Node Embedding, Global Sample Graph, Clone Detection},
location = {<conf-loc>, <city>San Francisco</city>, <state>CA</state>, <country>USA</country>, </conf-loc>},
series = {ESEC/FSE 2023}
}
```