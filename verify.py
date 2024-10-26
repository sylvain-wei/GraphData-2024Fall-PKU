"""verify the consistency of the node labels and the topology of the graph"""
import numpy as np
import time

def verify(data_graph, query_graph, Ms, verify_edge_label=True):
    """verify whether the data graph and query graph are isomorphic, by checking the node labels and the topology"""
    need_to_delete = []
    print(len(Ms))
    for idx_M, M in enumerate(Ms):  # 遍历每一个mapping matrix，因为有最多C(m, n)个mapping matrix
        # 1.check the node labels, not needed because of the LDF filter
        # 2.check the topology
        # 2.1 compute the MC matrix
        # M是n*m的矩阵，n是查询图的节点数，m是数据图的节点数
        # data_graph['adj_matrix']是m*m的矩阵
        MC = M @ (M @ data_graph['adj_matrix']).T   # 两次矩阵乘法，第一次O(n*m*m)，第二次O(n*m*n)，所以复杂度为O(n*m*(m+n))
        verifiable = True
        
        # get all ajacent nodes of the query graph  复杂度O(n*n)
        for idx, row in enumerate(query_graph['adj_matrix']):   # 复杂度O(n)
            for idx_, value in enumerate(row):  # 复杂度O(n)
                if value == 1 and MC[idx, idx_] == 0:
                    verifiable = False
                    break
                
        # 3.check the edge labels   复杂度O(n*n*m)
        if verifiable and verify_edge_label:
            for idx, row in enumerate(query_graph['adj_matrix']):   # 复杂度O(n)
                for idx_, value in enumerate(row):  # 复杂度O(n)
                    if value == 1:
                        if query_graph['edge_labels'][idx, idx_] != data_graph['edge_labels'][np.where(M[idx]==1), np.where(M[idx_]==1)]:   # 复杂度O(m)
                            verifiable = False
                            break
        if not verifiable:
            need_to_delete.append(idx_M)
    Ms = [Ms[idx] for idx in range(len(Ms)) if idx not in need_to_delete]
    return Ms