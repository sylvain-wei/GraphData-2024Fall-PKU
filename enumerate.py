import numpy as np
import copy
def convert_to_mapping_matrices(list_C_u, num_nodes_query, num_nodes_data):
    """get the mapping matrices, M's"""
    # 回溯得到所有的mapping matrices
    Ms = []
    unselected = copy.deepcopy(list_C_u)
    selected = []
    idx = 0     # 已经处理了的节点数
    while True:
        if idx == num_nodes_query:  # 完成一次搜索，记录M并回退
            M = np.zeros((num_nodes_query, num_nodes_data))
            for i in range(num_nodes_query):
                M[i][selected[i]] = 1
            Ms.append(M)
            # 回退
            idx -= 1    # 回退到上一个节点
            selected.pop()  # 已经搜索的节点也回退
        elif len(unselected[idx]) == 0: # 已经选择idx个节点后，候选空间为空，回退
            if idx == 0:
                break   # 已经回退到第一个节点，搜索结束
            unselected[idx] = copy.deepcopy(list_C_u[idx]) # 重新加入候选节点
            idx -= 1
            selected.pop()
        else:
            # 已经选择了idx个节点之后，还有可以搜索到的节点
            while len(unselected[idx]) > 0: # 单射限制：保证M中，每列只选择一个节点
                if unselected[idx][0] not in selected:
                    selected.append(unselected[idx][0])
                    unselected[idx].pop(0)
                    idx += 1
                    break
                else:   # 如果已经选择了该节点，直接pop
                    unselected[idx].pop(0)
    return Ms

def enumerate(data_graph, query_graph, list_C_u):
    """
    Plan phase
    """
    num_nodes_query = len(query_graph['node_labels'])
    num_nodes_data = len(data_graph['node_labels'])
    Ms = convert_to_mapping_matrices(list_C_u, num_nodes_query, num_nodes_data)
    return Ms