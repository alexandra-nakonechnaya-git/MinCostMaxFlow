"""
Created on Mon Apr 15 21:34:17 2019

@author: A.Nakonechnaya
"""

import sys
from utils import edges_from_csv,sup_dem_from_csv,Mapper
from algorithm import MCF, Edge


def main():

    input_NPZNB_file_name = "npz-nb.csv"
    input_NBNB_file_name = "nb-nb.csv"
    input_NBAZS_file_name = "nb-azs.csv"
    input_NPZAZS_file_name = "npz-azs.csv"
    input_supply_demand_file_name = "sup-dem.csv"
    out_csv_file_name = "out.csv"
    out_info_file_name = "info.txt"
    
    edgesNPZNB = edges_from_csv(input_NPZNB_file_name)
    edgesNBNB = edges_from_csv(input_NBNB_file_name)
    edgesNBAZS = edges_from_csv(input_NBAZS_file_name)
    edgesNPZAZS = edges_from_csv(input_NPZAZS_file_name)
    supply, demand, capacity = sup_dem_from_csv(input_supply_demand_file_name)

    print("Solving for: numEdges={}".format(len(edgesNPZNB+edgesNBAZS+edgesNPZAZS+edgesNBNB)))
    print("supply ={}, demand ={}".format(supply, demand))

    # отображать метки узлов как целые числа от 1 до n
    # Реализация MCMF требует, чтобы мы использовали от 0 до n для меток узлов, чтобы
    # удобно было использовать матрицы для весов, потоков и т. д.
    # При выводе ответа получим инверсию меток узлов.
    
    mapper = Mapper(1)

    edgesNPZ_NBmapped = [(mapper.mapQ(e[0]), mapper.mapP(e[1]), e[2])
                                                              for e in edgesNPZNB]
    edgesNB_NBmapped = [(mapper.mapP(e[0]), mapper.mapP(e[1]), e[2])
                                                              for e in edgesNBNB]
    edgesNB_AZSmapped = [(mapper.mapP(e[0]), mapper.mapU(e[1]), e[2])
                                                              for e in edgesNBAZS]
    edgesNPZ_AZSmapped = [(mapper.mapQ(e[0]), mapper.mapU(e[1]), e[2])
                                                              for e in edgesNPZAZS]
    
    unique_qs = set(mapper.qs.values())
    all_qs = list(unique_qs)
    unique_us = set(mapper.us.values())
    all_us = list(unique_us)
    all_us = sorted(all_us)   #confusing undefined bug
    unique_bs = set(mapper.bs.values())
    all_bs = list(unique_bs)
    n = len(all_qs) + len(all_us) +len(all_bs) + 1 + 1
    ## Назначаются первая и последняя метки узлов, то есть исток и сток.
    src_label = 0
    snk_label = n - 1

    desired_flow = 0.0 
    possible_flow = 0.0
 
    for i in range(len(demand)):
        desired_flow += demand[i]
    for i in range(len(supply)):
        possible_flow += supply[i]
         
    edgesNPZ_AZSdesired_flow = [(e[0], e[1], desired_flow, e[2])
                                                    for e in edgesNPZ_AZSmapped]
    edgesNPZ_NBdesired_flow = [(e[0], e[1], desired_flow, e[2])
                                                    for e in edgesNPZ_NBmapped]
    edgesNB_AZSdesired_flow = [(e[0], e[1], desired_flow, e[2])
                                                    for e in edgesNB_AZSmapped]

    sizeofList = len(edgesNB_NBmapped)
    edgesNB_NBdesired_flow = []
    i = 0
    while i< sizeofList:
        edgesNB_NBdesired_flow.append((edgesNB_NBmapped[i][0],edgesNB_NBmapped[i][1], \
                                                capacity[i], edgesNB_NBmapped[i][2])) 
        i += 1

    edges = edgesNPZ_NBdesired_flow + edgesNB_NBdesired_flow \
            + edgesNB_AZSdesired_flow + edgesNPZ_AZSdesired_flow
    num_edges_in_the_middle = len(edges)

    i = 0
    for q in all_qs:
        edges.append((src_label, q, supply[i], 0)) # src -> q (cap: h, cost: 0)
        i += 1
    i = 0
    for u in all_us:
        edges.append((u, snk_label, demand[i], 0)) # u -> snk (cap: h, cost: 0)
        i += 1

    edge_list = [Edge(e[0], e[1], e[2], e[3]) for e in edges]

    # Максимальный поток минимальной стоимости
    mcf = MCF(n, edge_list)
    flow, min_cost = mcf.min_cost_flow(desired_flow, src_label, snk_label)

    assigned_u_grouped_by_q = {}

    for i in range(num_edges_in_the_middle):
        e = mcf.edges[i]
        q = e.fr
        u = e.to
        c = mcf.capacity[q][u]

        if  0.0 < c < desired_flow :
            if assigned_u_grouped_by_q.get(q, None) is None:
                assigned_u_grouped_by_q[q] = []
            assigned_u_grouped_by_q[q].append(u)
    
    with open(out_csv_file_name, "w") as f:
         for q in assigned_u_grouped_by_q.keys():
            assigned_u_grouped_by_q[q] = sorted(assigned_u_grouped_by_q[q])
            for u in assigned_u_grouped_by_q[q]:
                f.write("{} --> {}".format(mapper.invQBU(q), mapper.invQBU(u)))
                f.write("   passed flow= {}\n".format(desired_flow - mcf.capacity[q][u]))
    
    with open(out_info_file_name, "w") as f:
        total_benefit = min_cost
        f.write("Value of left cut: |Q|.h = {}\n".format(possible_flow))
        f.write("Value of right cut: |U|.l = {}\n".format(desired_flow))
        f.write("Total flow sent: {}\n".format(flow))
        f.write("Min cost: {}\n".format(total_benefit))
        if flow > 0:
            f.write("Min cost per flow: {}\n".format(total_benefit/flow))



if __name__ == "__main__":
    main()