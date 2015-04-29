# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:22:53 2015

@author: aitor
"""
import operator
import numpy as np

import similarity

# These profiles have to be recovered from the social network
# These profiles are all from the same location
def matchmaking(profiles):
    users = {}
    total_socialization = []
    for profile in profiles:
        # ver como nos devuelve el profile la SN y crear el diccionario de users
        # Diccionario seria:
        #{'pepito' : {
        #    'activeness' : 23.2,
        #    'socialization' :  12.1,
        #    'hobbies' : ['a', 'b'],
        #    'connections' : ['aitor', 'aritz'],}}
        
        socialization = profile['socialization']
        # the socialization levels from all the users
        total_socialization.append(socialization)
    
    # The min socialization level is the 10% of the socilizations  
    a = np.array(total_socialization)    
    min_socialization = np.percentile(a, 10)
    
    recommendations = {}
    for u in users:
        user = users[u]
        # if the user socialization is low
        if user['socialization'] <= min_socialization:
            # find connections for the user
            connections = _find_connections(u, user, users)
            sorted_conns = sorted(connections.items(), key=operator.itemgetter(1))
            # get top 3 recommendations
            cont = 0
            recs = []
            for conn in sorted_conns:
                if cont < 3:
                    cont += 1
                    recs.append(conn[0])
            # if there are recommendations add it to the dict
            if len(recs) > 0:
                recommendations[u] = recs
                
    return recommendations        
   
            
def _find_connections(id1, user1, users):
    connections = {} # {'aitor' : 10, 'aritz' : 30}
    for id2 in users:
        user2 = users[id2]
        if id2 != id1:
            S = similarity.get_similarity(user1, user2)
            connections[id2] = S
            
    return connections
        
    
    