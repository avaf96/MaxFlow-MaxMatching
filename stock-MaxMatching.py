from operator import truediv
from sys import flags
from typing import List
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
import time



# dfs algorithm for allocating nodes
def allocating_dfs(current_stock,adjacency_mtrx,allocated,matched_stocks):
    if current_stock == -1:
      return True
    for stc in adjacency_mtrx[current_stock]:
      if allocated[stc]:
        continue
      allocated[stc] = True
      if allocating_dfs(matched_stocks[stc],adjacency_mtrx,allocated,matched_stocks):
        matched_stocks[stc] = current_stock
        return True

    return False



# maximum matching algorithm in bipartite graph using dfs algorithm for allocating nodes
def maximum_matching(n,k,stocks_list):
    adjacency_mtrx = []
    for i in range(n):
        temp1 = []
        for j in range(n):
          ct = 0
          for z in range(k):
            if stocks_list[i][z] < stocks_list[j][z]:
              ct+=1
          if ct == k:
            temp1.append(j)
        adjacency_mtrx.append(temp1)

    matched_stocks = [-1 for i in range(n)] 
    for i in range(n):
      allocated = [False for i in range(n)]
      allocating_dfs(i , adjacency_mtrx, allocated, matched_stocks)

    chart_num = 0
    for stock in matched_stocks:
      if stock == -1:
        chart_num+=1
   
    return matched_stocks,chart_num



# find stocks which can be in a same overlaid chart
def overlaid_lists(matched_stocks,min_chart_num):
    allocated = [False for i in range(n)]
    overlaid_dict = {}
    cnt = 0
    for stock in matched_stocks:
      if stock==-1:
        cnt+=1
    if cnt == len(matched_stocks):
      for i in range(min_chart_num):
        overlaid_dict[i] = list()
        overlaid_dict[i].append(i)
        allocated[i] = True
    else:
      for i in range(len(matched_stocks)):
        if matched_stocks[i]!= -1:
          if not overlaid_dict:
            allocated[i] = True
            allocated[matched_stocks[i]] =True
            overlaid_dict[0] = list()
            overlaid_dict[0].append(i)
            overlaid_dict[0].append(matched_stocks[i])
          else:
            for key in overlaid_dict.copy():
              if i in overlaid_dict[key] and allocated[matched_stocks[i]]==False:
                overlaid_dict[key].append(matched_stocks[i])
                allocated[matched_stocks[i]] =True
                break
              elif matched_stocks[i] in overlaid_dict[key] and allocated[i]==False:
                overlaid_dict[key].append(i)
                allocated[i] = True
                break
              elif (i in overlaid_dict[key] and allocated[matched_stocks[i]]==True) or (matched_stocks[i] in overlaid_dict[key] and allocated[i]==True):
                break

          flag = False 
          for w in range(len(overlaid_dict)):
            if i not in overlaid_dict.copy()[w] and matched_stocks[i] not in overlaid_dict.copy()[w]:
              continue
            else: 
              flag = True 
              break
          if flag==False:
            for j in range(min_chart_num):
              if j not in overlaid_dict.copy():
                overlaid_dict[j] = list()
                overlaid_dict[j].append(i)
                overlaid_dict[j].append(matched_stocks[i])
                allocated[i] = True
                allocated[matched_stocks[i]] =True
                break

      for stock in allocated.copy():
        if stock==False:
          for p in range(min_chart_num):
            if p in overlaid_dict:
              continue
            else:
              overlaid_dict[p] = list()
              overlaid_dict[p].append(allocated.index(stock))
              allocated[allocated.index(stock)] = True
              break         
    return overlaid_dict


# print overlaid charts one by one
def print_charts(overlaid_charts,stocks):  
    for key in overlaid_charts:
      G = nx.Graph()
      points = []
      edges = []
      points_len_before = 0
      for stock in overlaid_charts[key]:
        temp_list = stocks[stock]
        for index,point in enumerate(temp_list):
          points.append((index+1,point))
     
        if overlaid_charts[key].index(stock) == 0:
          for i in range(points_len_before,len(points)):
            if i != (len(points)-1):
              edges.append((i,i+1))
        else:
          for i in range(points_len_before,len(points)):
            if i != (len(points)-1):
              edges.append((i,i+1))
        points_len_before+=len(points)

      for i in range(len(edges)):
        G.add_edge(points[edges[i][0]],points[edges[i][1]])
      pos = {point: point for point in points}
      node_label= {}
      fig, ax = plt.subplots()
      nx.draw(G, pos=pos, node_size=10,node_color='r', ax=ax ,with_labels=False)  
      plt.axis("on")
      ax.yaxis.set_ticks(np.arange(0, 10, 1))
      ax.xaxis.set_ticks(np.arange(0, k+1 , 1))
      ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
      plt.show()



# read files
dir = "C:\\Users\\Desktop\\stock_charts\\inst"
for path in os.listdir(dir):   
    full_path = os.path.join(dir, path)
    first_line =[]
    stocks = []
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
      stocks.append(temp)
    n = first_line[0] 
    k = first_line[1]
    

    # call algorithm to find minimum number of overlaid charts and stocks in each overlaid chart
    start_time = time.time()
    matched_stocks , min_chart_num = maximum_matching(n,k,stocks)
    overlaid_charts = overlaid_lists(matched_stocks,min_chart_num)
    end_time = time.time() 
    
    print ("instance ", path , ">   min-overlaid-charts:" ,   min_chart_num  , "  time: ", end_time - start_time)


    # plot overlaid charts for each instance
    print_charts(overlaid_charts,stocks)


    # save overlaid charts lists and minimum number of overlaid charts in a different file for each instance
    with open("C:\\Users\\Desktop\\stock_charts\\stocks-result\\" + path + ".txt" , 'w') as f:
      f.write(f'\n\t**Minimum-overlaid-charts: {min_chart_num}')
      f.write(f'\n\t**Time: {end_time - start_time}')
      f.write("\n_______________________________________________\n")
      for i in range(len(overlaid_charts)):
        tmp = f'\n**chart {i}: {overlaid_charts[i]}'
        f.write(tmp)
    f.close()

   










