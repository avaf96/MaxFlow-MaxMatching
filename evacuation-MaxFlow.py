from sys import api_version
import time
import os
from turtle import pos
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network


# labeling augmenting path algorithm function for finding maximum flow
def labeling_aug_path_algo(graph , source, sink, num_of_nodes ):
	aug_paths = []
	aug_paths_flow = []
	parent = [" " for i in range(num_of_nodes)]   
	max_flow = 0								
	a_path = True
	while (a_path == True) :					
		a_path = False
		visited = [False for i in range(num_of_nodes)]    
		labeled = []								    
		labeled.append(source)							
		visited[source] = True
		while labeled:									
			u = labeled.pop(0)
			if u in graph:							
				for v in graph[u].copy():	
					if visited[v] == False:
						if v in graph[u]:
							for c in graph[u][v]:
								if c > 0:
									labeled.append(v)					
									visited[v] = True					 
									parent[v] = u						
									if v == sink:
										a_path = True
										current_path_flow = float("inf")
										t = sink
										temp = []
										while(t != source):
											for i in range(len(graph[parent[t]][t])):
												if (graph[parent[t]][t][i] != 0):
													current_path_flow = min (current_path_flow, graph[parent[t]][t][i])		
											temp.append(t)															 
											t = parent[t]																																				
										max_flow += current_path_flow
										temp.append(source)
										temp.reverse()
										aug_paths.append(temp)	
										aug_paths_flow.append(current_path_flow)									
										v = sink
										while(v != source):
											u = parent[v]
											if v not in graph:
												graph[v] = {}
											for i in range(len(graph[u][v])):
												if (graph[u][v][i] >= current_path_flow):
													graph[u][v][i] -= current_path_flow	
													if u not in graph[v]:	
															graph[v][u] = list()
															graph[v][u].append(current_path_flow)	
													else:
														graph[v][u][0] += current_path_flow
													v = parent[v]
													break
									break
							

	return max_flow,graph,aug_paths,aug_paths_flow




# print initial graph function
def print_initial_graph(graph , num_of_nodes):
	G = nx.MultiDiGraph()
	for i in range(num_of_nodes):
		G.add_node(i , label= str(i))
	for i in range(num_of_nodes):
		u = i
		if u in graph:
			for j in range(num_of_nodes):
				v = j
				if v in graph[u]:
					for k in range(len(graph[u][v])):
						c = graph[u][v][k]
						if c > 0 :
							G.add_edge(u,v,label= str(c))
	nt = Network(directed=True)
	nt.from_nx(G)
	nt.set_edge_smooth('dynamic')
	nt.show('graph.html')



# print final residual graph function
def print_final_residual_graph(graph , num_of_nodes):
	G = nx.MultiDiGraph()
	for i in range(num_of_nodes):
		G.add_node(i)
	for i in range(num_of_nodes):
		u = i
		if u in graph:
			for j in range(num_of_nodes):
				v = j
				if v in graph[u]:
					for k in range(len(graph[u][v])):
						c = graph[u][v][k]
						if c > 0 :
							G.add_edge(u,v,length= c)
	pos = nx.spring_layout(G)
	nx.draw(G, pos  ,with_labels=True)
	edge_labels=dict([((u,v,),d['length'])
				for u,v,d in G.edges(data=True)])
	nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3, font_size=10 )
	plt.show()



# print augmenting paths one by one
def print_aug_paths(augPaths,augPaths_flow):
	for i in range(len(augPaths)):
		G = nx.MultiDiGraph()
		for j in range(len(augPaths[i])):
			if ( j != len(augPaths[i])-1):
				u = augPaths[i][j]
				v = augPaths[i][j+1]
				f = augPaths_flow[i]
				G.add_edge(u,v,length= f)
		pos = nx.spring_layout(G)
		nx.draw(G, pos  ,with_labels=True)
		edge_labels2=dict([((u,v,),d['length'])
					for u,v,d in G.edges(data=True)])
		nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels2, label_pos=0.3, font_size=10 )
		plt.show()




# read files
dir = "C:\\Users\\Desktop\\evacuation\\inst"
for path in os.listdir(dir):
	full_path = os.path.join(dir, path)
	first_line =[]
	matrix = []
	file_lines= ""
	with open(full_path, "r") as f:
		for i in f.readline().replace("\n" , "").split():
			first_line.append(int(i))
		file_lines = f.readlines()
	f.close()

	for line in file_lines:
		temp = []
		for i in line.replace("\n" , "").split():
			temp.append(int(i))
		matrix.append(temp) 



    # creating an initial graph using dictionary
	graph = {}
	for i in range(0,len(matrix)):
		src = matrix[i][0] - 1
		dict_temp = {}
		for j in range(0,len(matrix)):
			if ((matrix[j][0]-1) == src):
				dest = matrix[j][1] - 1
				cap = matrix[j][2]
				if dest not in dict_temp:
					dict_temp[dest] = list()
				dict_temp[dest].append(cap)
		graph[src] = dict_temp



	# plot initial graph
	# print_initial_graph(graph,first_line[0]) 



	# call labeling algoritm function and print the result
	source = 0
	sink = first_line[0]-1
	start_time = time.time()
	maxFlow,gr,augPaths,augPaths_flow = labeling_aug_path_algo(graph, source, sink , first_line[0])
	end_time = time.time() 
	print ("instance ", path , ">   max-flow: " , maxFlow , "      time: ", end_time - start_time )


	# plot augmenting paths and their corresponding flow
	# print_aug_paths(augPaths,augPaths_flow)


	# save augmenting paths and maximum flow in a different file for each instance
	with open("C:\\Users\\Desktop\\evacuation\\evacuation-results\\" + path + ".txt" , 'w') as f:
		f.write(f'\n\t**Maximum-Flow: {maxFlow}')
		f.write(f'\n\t**Time: {end_time - start_time}')
		f.write("\n_______________________________________________\n")
		for i in range(len(augPaths)):
			tmp = f'**Aug-Path({i}): {augPaths[i]}  \n**Flow: {augPaths_flow[i]}'
			f.write(tmp)
			f.write("\n_______________________________________________\n")
	f.close()


	# plot final residual graph
	# print_final_residual_graph(gr ,first_line[0])
	