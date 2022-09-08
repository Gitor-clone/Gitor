# Gitor

We propose \emph{Gitor} to capture the underlying connections (\ie \emph{global information}) among different code samples. Specifically, given a source code database, we first tokenize all code samples to extract the pre-defined \emph{global information} (\eg \emph{keywords}). After obtaining all samples' global information, we leverage them to build a large \emph{global sample graph} where each node is a code sample or a type of global information. Then we apply a node embedding technique on the global sample graph to extract all samples' vector representations. After collecting all code samples' vectors, we can simply compare the similarity between any two samples to detect possible clone pairs. More importantly, since the obtained vector of a sample is from a global sample graph, we can combine it with its code features to improve the code clone detection performance.

The Gitor mainly consists of four phases:

extract.py: Used to extract global information (Keywords) from code samples.\
side_info.py: Used to extract side information from code samples.\
train.py: Used for node embedding.\
detect.py: Used for code clone detection.

The source code and dataset of Gitor will be published here after the paper is accepted.
