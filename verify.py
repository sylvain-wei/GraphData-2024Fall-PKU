"""verify the consistency of the node labels and the topology of the graph"""
import numpy as np
import time

def verify(data_graph, query_graph, Ms, verify_edge_label=True):
    """verify whether the data graph and query graph are isomorphic, by checking the node labels and the topology"""
    need_to_delete = []
    print(len(Ms))
    for idx_M, M in enumerate(Ms):
        # print('idx_M', idx_M, 'len(Ms):', len(Ms))
        # 1.check the node labels, not needed because of the LDF filter
        # 2.check the topology
        # 2.1 compute the MC matrix
        # time_start = time.time()
        # print(type(data_graph['adj_matrix']))
        MC = M @ (M @ data_graph['adj_matrix']).T
        # time_end = time.time()
        # print('MC time:', time_end-time_start)
        verifiable = True
        
        # get all ajacent nodes of the query graph
        for idx, row in enumerate(query_graph['adj_matrix']):
            for idx_, value in enumerate(row):
                if value == 1 and MC[idx, idx_] == 0:
                    verifiable = False
                    break
                
        # 3.check the edge labels
        if verifiable and verify_edge_label:
            for idx, row in enumerate(query_graph['adj_matrix']):
                for idx_, value in enumerate(row):
                    if value == 1:
                        if query_graph['edge_labels'][idx, idx_] != data_graph['edge_labels'][np.where(M[idx]==1), np.where(M[idx_]==1)]:
                            verifiable = False
                            break
        if not verifiable:
            need_to_delete.append(idx_M)
    Ms = [Ms[idx] for idx in range(len(Ms)) if idx not in need_to_delete]
    return Ms