"""Filtering functions for the data."""
# 目前Ullmann算法只考虑点的label和点的degree，所以只实现了LDF和NLF两种filter
# 之后可能要考虑边标签的映射

import numpy as np

def LDF_filter(data_graph, query_graph, list_C_u):
    """
    Label Degree Filter(Ullmann needed)
    复杂度，设查询图节点数为n，数据图节点数为m，查询图平均度数为d，数据图平均度数为D，则复杂度为O(n*m*d*D)
    """
    
    for idx, node_label in enumerate(query_graph['node_labels']):   # 遍历查询图中的每个节点O(n)
        # find graph nodes with the same label
        C_u = []
        for idx_, node_label_ in enumerate(data_graph['node_labels']):  # 遍历数据图中的每个节点O(m)
            if node_label == node_label_:
                # check the degree of the nodes
                if np.sum(data_graph['adj_matrix'][idx_]) >= np.sum(query_graph['adj_matrix'][idx]):
                    C_u.append(idx_)
        list_C_u.append(C_u)
    return list_C_u
    

def NLF_filter(data_graph, query_graph, list_C_u):
    """
    Neighborhood Label Filter
    复杂度，设查询图节点数为n，数据图节点数为m，查询图平均度数为d，数据图平均度数为D，则复杂度为O(n*(d+m*D))
    """
    for idx, C_u in enumerate(list_C_u):    # 遍历查询图中的每个节点O(n)
        check_dict_query_node = {} # 用于存储查询图当前节点的邻居节点的label映射
        for n_idx in np.where(query_graph['adj_matrix'][idx] == 1)[0]:  # 遍历查询图中idx的邻居节点O(d)
            n_label = query_graph['node_labels'][n_idx]
            check_dict_query_node[n_label] = check_dict_query_node[n_label] + 1 if n_label in check_dict_query_node else 0
        for idx_ in C_u:    # 遍历数据图中的每个节点O(m)
            # check the neighborhood label
            for n_idx_ in np.where(data_graph['adj_matrix'][idx_] == 1)[0]:
                n_label_ = data_graph['node_labels'][n_idx_]
                if n_label_ in check_dict_query_node:
                    check_dict_query_node[n_label_] -= 1
            delete = False
            for key, value in check_dict_query_node.items():    # 遍历查询图当前节点的邻居节点的label映射O(d)
                if value > 0:
                    delete = True
                    break
            if delete:
                # 删除不符合条件的节点
                list_C_u[idx].remove(idx_)
    return list_C_u

def neighbourhood_connection_prunning(data_graph, query_graph, list_C_u):
    """
    Neighborhood Connection Prunning 主要考虑拓扑结构
    时间复杂度，设查询图节点数为n，数据图节点数为m，查询图平均度数为d，数据图平均度数为D，则复杂度为O(n*m*d*D)
    """
    for idx, C_u in enumerate(list_C_u):    # 遍历查询图中的每个节点O(n)
        for idx_ in C_u:    # 遍历数据图中的每个节点O(m)
            # check the neighborhood connection
            for n_idx in np.where(query_graph['adj_matrix'][idx] == 1)[0]: # 遍历查询图中idx的邻居节点O(d)
                save = False
                for n_idx_ in np.where(data_graph['adj_matrix'][idx_] == 1)[0]: # 遍历数据图中idx_的邻居节点O(D)
                    if n_idx_ in list_C_u[n_idx]: # 如果数据图中idx_的邻居节点在查询图中idx的邻居节点的候选集中
                        if query_graph['edge_labels'][idx][n_idx] == data_graph['edge_labels'][idx_][n_idx_]:   # 并且要求边标签相同
                            save = True
                            break
                if not save:
                    list_C_u[idx].remove(idx_)
                    break
    return list_C_u

def filter_and_plan(data_graph, query_graph, LDF=True, NLF=False, prunning=True):
    """
    Filtering, including basic mapping, LDF and NLF. And then return the list of mapping matrices.
    """
    list_C_u = []   # 用于存储每个节点的候选集
    assert NLF or LDF, "At least one filter should be used."
    if LDF:
        list_C_u = LDF_filter(data_graph, query_graph, list_C_u=[])
    if NLF:
        list_C_u = NLF_filter(data_graph, query_graph, list_C_u=list_C_u)
    if prunning:
        list_C_u = neighbourhood_connection_prunning(data_graph, query_graph, list_C_u)
    
    return list_C_u