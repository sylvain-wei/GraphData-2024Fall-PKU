# Ullmann Algorithm for Subgraph Isomorphism
# Shaohang Wei @ School of CS, PKU
# Reference: J.R. Ullmann, An Algorithm for Subgraph Isomorphism, Journal of the ACM, 23(1):31-42, 1976

from filter_and_plan import *
from enumerate import *
from verify import *
from utils import *

import numpy as np
import argparse
import os
import json
import time

def set_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='graphDB/mygraphdb.data', help='data file path')
    parser.add_argument('--query', type=str, default='graphDB/Q24.my', help='query file path')
    parser.add_argument('--verify_edge_label', action="store_true", help='whether to verify the edge labels, default is False')
    parser.add_argument('--prunning', action="store_false", help='whether to prunning by neighborhood connection, default is True')
    return parser.parse_args()

def subgraph_match(data_graph, query_graph):
    """
    Subgraph isomorphism; three phases
    return: list of mappings(query_dot to data_dot)
    """
    # phase 1: filter and plan
    time_all_start = time.time()
    time_start = time.time()
    list_C_u = filter_and_plan(data_graph, query_graph, LDF=True, NLF=True, prunning=args.prunning)
    time_end = time.time()
    time_filter_plan.append(time_end-time_start)
    # phase 2: enumerate all the possible mappings
    time_start = time.time()
    Ms = enumerate(data_graph, query_graph, list_C_u)
    time_end = time.time()
    time_enumerate.append(time_end-time_start)
    # phase 3: verify all the mappings through node label and topology
    time_start = time.time()
    Ms = verify(data_graph, query_graph, Ms, verify_edge_label=args.verify_edge_label)
    time_end = time.time()
    time_verify.append(time_end-time_start)
    time_subgraph_match.append(time_end-time_all_start)
    
    # convert the mapping matrices to the list of node mappings
    mappings = []
    for M in Ms:
        mapping = {}
        for idx in range(len(M)):
            idx_ = int(np.where(M[idx] == 1)[0][0])
            mapping[idx] = idx_
        mappings.append(mapping)
    return mappings

if __name__ == '__main__':
    args = set_args()
    
    data_graphs = read_graphs(args.data)
    query_graphs = read_graphs(args.query)
    num_data_graphs = len(data_graphs.items())
    num_query_graphs = len(query_graphs.items())
    print(f"Query graphs: from {args.query}, which has {num_query_graphs} graphs")
    print(f"Data graphs: from {args.data}, which has {num_data_graphs} graphs")

    all_matches = []
    time_filter_plan = []
    time_enumerate = []
    time_verify = []
    time_subgraph_match = []
    for qid, query_graph in query_graphs.items():
        for did, data_graph in data_graphs.items():
            print(f"Query graph {qid} against data graph {did}")
            result = subgraph_match(data_graph, query_graph)
            match_result = {
                'graph_pairs': (qid, did),
                '#_matches': len(result),
                'verify_edge_label': args.verify_edge_label,
                'result': result
            }  # list of mappings, each mapping is a dict
            print(f"Isomorphism result: {result}")
            print()
            all_matches.append(match_result)
    
    with open(f'results/match_result_{os.path.basename(args.query)}_{os.path.basename(args.data)}'+('_verify_edge_label' if args.verify_edge_label else '')+'.json', 'w') as f:
        json.dump(all_matches, f, indent=4, ensure_ascii=False)
        
    print("time_filter_plan:", np.mean(time_filter_plan))
    print("time_enumerate:", np.mean(time_enumerate))
    print("time_verify:", np.mean(time_verify))
    print("time_subgraph_match:", np.mean(time_subgraph_match))