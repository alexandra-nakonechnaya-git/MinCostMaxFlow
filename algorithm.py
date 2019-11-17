#!/usr/bin/env python3
import collections
import csv
import sys

# INF = 10 ** 18

class Edge():
    def __init__(self, fr, to, capacity, cost):
        self.fr = fr
        self.to = to
        self.capacity = capacity
        self.cost = cost

    def __str__(self):
        return "fr: {}, to: {}, cap: {}, cost: {}".format(self.fr, self.to,
                self.capacity, self.cost)


class MCF():
    def __init__(self, n, edges):
        self.edges = edges
        self.n = n

    def minDist(self, mdist, vset):
	    minVal = float('inf')
	    minInd = -1
	    for i in range(self.n):
	    	if (not vset[i]) and mdist[i] < minVal :
	    		minInd = i
	    		minVal = mdist[i]
	    return minInd

    def shortest_paths(self, v0):
        mdist = [float('inf') for i in range(self.n)]
        vset = [False for i in range(self.n)]
        p = [-1 for i in range(self.n)]
        mdist[v0] = 0.0

        for i in range(self.n-1):
            u = self.minDist(mdist, vset)
            vset[u] = True
            for v in self.adj[u]:
                if self.capacity[u][v] > 0 \
                    and  mdist[u] + self.cost[u][v] < mdist[v]:
                    mdist[v] = mdist[u] + self.cost[u][v]
                    p[v] = u
           
        return mdist, p

        

    def min_cost_flow(self, desired_flow, s, t):
        self.adj = [[] for i in range(self.n)]
        self.cost = [[0] * self.n for i in range(self.n)]
        self.capacity = [[0] * self.n for i in range(self.n)]

        for e in self.edges:
            self.adj[e.fr].append(e.to)

            self.cost[e.fr][e.to] = e.cost
            self.capacity[e.fr][e.to] = e.capacity

        flow, cost = 0, 0
        d, p = [], []
        while flow < desired_flow:
            d, p = self.shortest_paths(s)
            if d[t] == float('inf'):
                break

            f = desired_flow - flow
            cur = t
            while cur != s:
                f = min(f, self.capacity[p[cur]][cur])
                cur = p[cur]

            flow += f
            cost += f * d[t] #tbd d[t] -!!!
            cur = t
            while cur != s:
                self.capacity[p[cur]][cur] -= f
                cur = p[cur]

         #   print(p[p[t]],"->",p[t]," :: ", flow)

        return flow, cost
