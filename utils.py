"""
Created on Sun Apr 14 17:04:43 2019

@author: A.Nakonechnaya
"""
# import networkx as nx
# import matplotlib.pyplot as plt
# import pylab
import os.path
import csv

class Mapper():
    def __init__(self, start_from):
        self.qs = {}
        self.us = {}
        self.bs = {}
        self.qbus = {}
        self.invUs = {}
        self.invQs = {}
        self.invBs = {}
        self.invQBUs = {}
        self.next_node = start_from

    def _map(self, mp, inv_mp, key):
        val = mp.get(key, None)
        if val is None:
            val = self.next_node
            mp[key] = val
            self.qbus[key] = val
            inv_mp[val] = key
            self.invQBUs[val] = key
            self.next_node += 1
        return val

    def mapQ(self, q):
        return self._map(self.qs, self.invQs, q)

    def mapU(self, u):
        return self._map(self.us, self.invUs, u)

    def mapP(self, b):
        return self._map(self.bs, self.invBs, b)   

    def _inv(self, inv_map, mapped):
        return inv_map[mapped]

    def invQ(self, mappedQ):
        return self._inv(self.invQs, mappedQ)

    def invU(self, mappedU):
        return self._inv(self.invUs, mappedU)

    def invB(self, mappedB):
        return self._inv(self.invBs, mappedB)

    def invQBU(self, mappedQBU):
        return self._inv(self.invQBUs, mappedQBU)

        
def edges_from_csv(file_name):
    """Читается CSV-файл, содержащий столбцы Q, V, Probability, соответствующие
    ребра Q-U. Предполагается, что сначала приходит  Q, затем U, 
    а затем - вес ребра."""
    if(os.path.isfile(file_name)):
        with open(file_name, "r") as csv_file:
            reader = csv.reader(csv_file)
            reader.__next__() # skip first string
            lines = [line for line in reader]
            edge_triples = [(str(line[0]), str(line[1]), float(line[2])) 
                          for line in lines]        
            return edge_triples
    else:
        edge_triples= []
        return edge_triples

def sup_dem_from_csv(file_name):
    """Читается CSV-файл, содержащий three строки «предложение, спрос, ».
    Чтение происходит с конца"""
    
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        reader.__next__() # skip first string

        lines = [line for line in reader]
        supply = [(float(row)) for row in lines[0]]
        demand = [(float(row)) for row in lines[1]]
        if (len(lines) == 3):
            capacity = [(float(row)) for row in lines[2]]
        else:
            capacity =[]
        return supply, demand, capacity
    
"""    
def draw(edges):
    
    G = nx.DiGraph()
    G.add_weighted_edges_from([(e[0], e[1], e[3]) for e in edges])
    edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])
    pos = {0:(0,2.5), 1:(2,0), 2:(2,5), 3:(4,0), 4:(4,2.5), 5:(4,5), 6:(6,2.5)}
#    pos=nx.spring_layout(G, pos= ipos)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
    nx.draw(G,pos, node_color = 'green', node_size=1500,edge_color='blue',edge_cmap=plt.cm.Reds)
    pylab.show()
"""