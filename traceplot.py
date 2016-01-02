import networkx as nx
import random
import numpy as np
from random import choice, random
import collections
import matplotlib.pyplot as plt


def CalculateCMu(X,G,C):
	sum=0
	div=0
	for i in range(0,len(X)):
		sum=sum+(float(C[X[i]])/G.degree(X[i]))
		div=div+(float(1)/G.degree(X[i]))
	return float(sum)/div

def runSRW(G,C):
	T=[]
	for i in range(0,10):
		X=[]
		startNode = G.nodes()[0]
		currentNode = startNode
		X.append(startNode)
		run=True
		while (run is True):
			nextNode=choice(G.neighbors(currentNode))
			currentNode=nextNode
			X.append(currentNode)
			if C[currentNode]> 4:
				run=False
		T.append(len(X))
	return np.mean(T)

def makeChoice(neighbors):
	communityArray=[]
	for neighbor in neighbors:
		communityArray.append(C[neighbor])
	cnt = collections.Counter()
	for word in communityArray:
		cnt[word] += 1
	chosen=choice(list(cnt))
	chosenArray=[]
	for neighbor in neighbors:
		if C[neighbor] is chosen:
			chosenArray.append(neighbor)
	chosenNode=choice(chosenArray)
	return chosenNode

def PurposePro(fromNode,toNode,C,G):
	toNodeCom=C[toNode]
	neighbors=G.neighbors(fromNode)
	communityArray=[]
	for neighbor in neighbors:
		communityArray.append(C[neighbor])
	cnt = collections.Counter()
	for word in communityArray:
		cnt[word] += 1
	firstProp=float(1)/len(list(cnt))
	secondProp=float(1)/cnt[toNodeCom]
	finalProp=firstProp*secondProp
	return finalProp

def runRW(G,C):
	T=[]
	for i in range(0,10):
		X=[]
		startNode = G.nodes()[0]
		currentNode = startNode
		X.append(startNode)
		run=True
		while (run is True):
			nextNode=makeChoice(G.neighbors(currentNode))
			PurposePro(currentNode,nextNode,C,G)
			a = float(G.degree(nextNode)*PurposePro(nextNode,currentNode,C,G))/ float(G.degree(currentNode)*PurposePro(currentNode,nextNode,C,G))
			r = np.random.uniform(0, 1)
			if r<a:
				currentNode=nextNode
			X.append(currentNode)
			if C[currentNode]> 4:
				run=False
		T.append(len(X))
	return np.mean(T)

def addEdges(G,start1,end1,start2,end2,number):
	for i in range(0,number):
		a=choice(range(start1, end1))
		b=choice(range(start2, end2))
		G.add_edge(a,b)
	return G


if __name__ == "__main__":
	Nvalue = []
	ResultN =[]
	ResultS =[]
	for n in range(1,11):
		Nvalue.append(5*50*n)
		C=[None]*(5*50*n)
		for i in range(0,50*n):
			C[i]=1
		for i in range(50*n,100*n):
			C[i]=2
		for i in range(100*n,150*n):
			C[i]=3
		for i in range(150*n,200*n):
			C[i]=4
		for i in range(200*n,250*n):
			C[i]=5


		G = nx.connected_caveman_graph(5,50*n)
		G.remove_edge(0,5*50*n-1)
		G=addEdges(G,1,50*n-1,50*n+1,100*n-1,3)
		G=addEdges(G,50*n+1,100*n-1,100*n+1,150*n-1,3)
		G=addEdges(G,100*n+1,150*n-1,150*n+1,200*n-1,3)
		G=addEdges(G,150*n+1,200*n-1,200*n+1,250*n-1,3)
		print n
		# ResultS.append(runSRW(G,C))
		ResultN.append(runRW(G,C))


	# plt.plot(Nvalue,ResultS,'b')

	plt.plot(Nvalue,ResultN,'r')
	plt.ylabel('T(n)')
	plt.xlabel('red line: new RW')
	plt.show()

