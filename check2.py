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

def runSRW(G,t,C):
	X=[]
	startNode = G.nodes()[0]
	currentNode = startNode
	X.append(startNode)
	for T in range(1,t):
		nextNode=choice(G.neighbors(currentNode))
		currentNode=nextNode
		X.append(currentNode)
	muN=CalculateCMu(X,G,C)
	return muN

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

def runRW(G,t,C):
	X=[]
	startNode = G.nodes()[0]
	currentNode = startNode
	X.append(startNode)
	# # walk start
	for j in range(1,t):
		nextNode=makeChoice(G.neighbors(currentNode))
		PurposePro(currentNode,nextNode,C,G)
		a = float(G.degree(nextNode)*PurposePro(nextNode,currentNode,C,G))/ float(G.degree(currentNode)*PurposePro(currentNode,nextNode,C,G))
		r = np.random.uniform(0, 1)
		if r<a:
			currentNode=nextNode
		X.append(currentNode)
	return CalculateCMu(X,G,C)

def addEdges(G,start1,end1,start2,end2,number):
	for i in range(0,number):
		a=choice(range(start1, end1))
		b=choice(range(start2, end2))
		G.add_edge(a,b)
		print [a,b]
	return G


if __name__ == "__main__":
	ResultN =[]
	ResultS =[]
	C=[None]*400
	for i in range(0,100):
		C[i]=1
	for i in range(100,200):
		C[i]=20
	for i in range(200,300):
		C[i]=50
	for i in range(300,400):
		C[i]=80

	G = nx.connected_caveman_graph(4,100)
	G.remove_edge(0,399)
	G=addEdges(G,1,99,101,199,3)
	G=addEdges(G,101,199,201,299,3)
	G=addEdges(G,201,299,301,399,3)
	print nx.diameter(G)
	#True Mu is 37.75
	for k in range(1,31):
		print 'SRW run to'
		print k
		S=[]
		tMu=37.75
		for m in range(0,10):
			S.append(runSRW(G,500*k,C))
		RE= float(np.sum(abs(np.subtract(S,tMu))))/10
		ResultS.append(RE)
	for k in range(1,31):
		print 'RW run to'
		print k
		S=[]
		tMu=37.75
		for m in range(0,10):
			S.append(runRW(G,500*k,C))
		RE= float(np.sum(abs(np.subtract(S,tMu))))/10
		ResultN.append(RE)
	plt.plot([500,1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000,8500,9000,9500,10000,10500,11000,11500,12000,12500,13000,13500,14000,14500,15000],ResultN,'r')
	plt.plot([500,1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000,8500,9000,9500,10000,10500,11000,11500,12000,12500,13000,13500,14000,14500,15000],ResultS,'b')
	plt.show()

