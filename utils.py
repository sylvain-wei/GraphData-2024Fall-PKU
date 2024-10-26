# some utils functions for reading and writing data
import numpy as np 

def read_graphs(fp):
    """read graphs from file fp"""
    """basic graph structure[dict]:
    node_labels: list[int], list of node labels;
    adj_matrix: np.array, adjacency matrix;
    edge_labels: np.array, edge labels
    """
    graphs = {}
    with open(fp, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('t'):
                graph_id = int(line.split()[2])
                if graph_id == -1:
                    break
                graphs[graph_id] = {}
                graphs[graph_id]['node_labels'] = []
                graphs[graph_id]['adj_matrix'] = None
                graphs[graph_id]['edge_labels'] = None
            if line.startswith('v'):
                node_id, node_label = line.split()[1:]
                graphs[graph_id]['node_labels'].append(int(node_label))
                last_is_node = True
            if line.startswith('e'):
                if last_is_node:
                    graphs[graph_id]['adj_matrix'] = np.zeros((len(graphs[graph_id]['node_labels']), len(graphs[graph_id]['node_labels'])))
                    graphs[graph_id]['edge_labels'] = np.zeros((len(graphs[graph_id]['node_labels']), len(graphs[graph_id]['node_labels'])))
                    last_is_node = False
                node1, node2, edge_label = line.split()[1:]
                node1, node2 = int(node1), int(node2)
                graphs[graph_id]['adj_matrix'][node1, node2] = 1
                graphs[graph_id]['adj_matrix'][node2, node1] = 1
                graphs[graph_id]['edge_labels'][node1, node2] = int(edge_label)
                graphs[graph_id]['edge_labels'][node2, node1] = int(edge_label)
    return graphs

if __name__ == '__main__':
    graphs = read_graphs('test.my')
    print(graphs)