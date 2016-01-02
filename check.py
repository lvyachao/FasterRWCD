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

if __name__ == "__main__":
	ResultN =[]
	ResultS =[]
	C=[None]*100
	for i in range(0,50):
		C[i]=1

	for j in range(50,100):
		C[j]=100

	G = nx.connected_caveman_graph(2, 50)
		# for node in G.nodes():
		# 	print G.neighbors(node)
	#True Mu is 50.5
	for k in range(1,11):
		print 'SRW run to'
		print k
		S=[]
		tMu=50.5
		for m in range(0,10):
			S.append(runSRW(G,1000*k,C))
		RE= float(np.sum(abs(np.subtract(S,tMu))))/10
		ResultS.append(RE)
	for k in range(1,11):
		print 'RW run to'
		print k
		S=[]
		tMu=50.5
		for m in range(0,10):
			S.append(runRW(G,1000*k,C))
		RE= float(np.sum(abs(np.subtract(S,tMu))))/10
		ResultN.append(RE)
	plt.plot([1000,2000,3000,4000,5000,6000,7000,8000,9000,10000],ResultN,'r')
	plt.plot([1000,2000,3000,4000,5000,6000,7000,8000,9000,10000],ResultS,'b')
	plt.xlabel('blue line: SRW, red line: NewRW')
	plt.show()

