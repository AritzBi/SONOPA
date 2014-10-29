# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 09:32:34 2014

@author: aitor
"""

import networkx as nx
from networkx.algorithms import bipartite
import community

class NetworkAnalyzer:
    
    def _calculate_connected_components(self, G):
        components = nx.weakly_connected_component_subgraphs(G)    

        for i, cc in enumerate(components):            
            #Set the connected component for each group
            for node in cc:
                G.node[node]['component'] = i
          
            #Calculate the in component betweeness, closeness and eigenvector centralities        
            cent_betweenness = nx.betweenness_centrality(cc)              
            cent_eigenvector = nx.eigenvector_centrality_numpy(cc)
            cent_closeness = nx.closeness_centrality(cc) 
            
            
            for name in cc.nodes():
                G.node[name]['cc-betweenness'] = cent_betweenness[name]
                G.node[name]['cc-eigenvector'] = cent_eigenvector[name]
                G.node[name]['cc-closeness'] = cent_closeness[name]
     
        return G
        
    def _calculate_centralities(self, G):
        out_degrees = G.out_degree()
        in_degrees = G.in_degree()
        betweenness = nx.betweenness_centrality(G)
        eigenvector = nx.eigenvector_centrality_numpy(G)
        closeness = nx.closeness_centrality(G)
        pagerank = nx.pagerank(G)
        avg_neighbour_degree = nx.average_neighbor_degree(G)
        redundancy = bipartite.node_redundancy(G)
        load = nx.load_centrality(G)
        hits = nx.hits(G)
        vitality = nx.closeness_vitality(G)
        
        for name in G.nodes():
            G.node[name]['out_degree'] = out_degrees[name]
            G.node[name]['in_degree'] = in_degrees[name]
            G.node[name]['betweenness'] = betweenness[name]
            G.node[name]['eigenvector'] = eigenvector[name]
            G.node[name]['closeness'] = closeness[name]
            G.node[name]['pagerank'] = pagerank[name]
            G.node[name]['avg-neigh-degree'] = avg_neighbour_degree[name]
            G.node[name]['redundancy'] = redundancy[name]
            G.node[name]['load'] = load[name]
            G.node[name]['hits'] = hits[name]
            G.node[name]['vitality'] = vitality[name]
            
        return G
        
    def _calculate_communities(self, G):
        G_undirected = G.to_undirected();        
        partitions = community.best_partition(G_undirected)
        for member, c in partitions.items():
            G.node[member]['community'] = c  
            
        return G
        

    def analyze_graph(self, G):    
        
        G = self._calculate_connected_components(G)
        G = self._calculate_centralities(G)
        G = self._calculate_communities(G)
                   
        return G