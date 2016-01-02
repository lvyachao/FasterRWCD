import networkx as nx
import random
import numpy as np
from random import choice, random
import collections
import matplotlib.pyplot as plt
import community


fh=open("dblp.txt",'rb')
G=nx.read_edgelist(fh,nodetype=int)


#first compute the best partition
partition = community.best_partition(G)

print partition