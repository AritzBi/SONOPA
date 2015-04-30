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
    for current_user in profiles:
        # ver como nos devuelve el profile la SN y crear el diccionario de users
        # Diccionario seria:
        #{'pepito' : {
        #    'activeness' : 23.2,
        #    'socialization' :  12.1,
        #    'hobbies' : ['a', 'b'],
        #    'connections' : ['aitor', 'aritz'],}}
        
        profile = profiles[current_user]
        users[current_user] = {
            'socialization' : profile['socialization'],
            'activeness' : profile['activeness'],
            'hobbies' : set(profile['hobbies']),
            'connections' : set(profile['connections'])           
        }
        
        socialization = profile['socialization']
        # the socialization levels from all the users
        total_socialization.append(socialization)
    
    # The min socialization level is the 30th percentile  
    a = np.array(total_socialization)    
    min_socialization = np.percentile(a, 30)
    
    recommendations = {}
    for u in users:
        user = users[u]
        # if the user socialization is low
        if user['socialization'] <= min_socialization:
            # find connections for the user
            connections = _find_connections(u, user, users)
            sorted_conns = sorted(connections.items(), key=operator.itemgetter(1), reverse=True)
            #print sorted_conns
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
            # Already a connection
            if id2 not in user1['connections']:
                #print id1, 'with', id2
                S = similarity.get_similarity(user1, user2)
                connections[id2] = S
            
    return connections
    
    
if __name__ == '__main__':
    test_profiles = {  'aritz' : {    'socialization' : 13.1,
                                      'activeness' : 223,
                                      'hobbies' : ['fishing', 'painting', 'movies'],
                                      'connections' : ['mikel', 'juan', 'oscar']    
                        },
                       'aitor' : {    'socialization' : 0.1,
                                      'activeness' : 222,
                                      'hobbies' : ['fishing', 'painting'],
                                       'connections' : ['mikel', 'juan', 'oscar']    
                        }, 
                        
                        'oscar' : {    'socialization' : 8.1,
                                      'activeness' : 112,
                                      'hobbies' : ['fishing', 'theater'],
                                       'connections' : ['mikel', 'aritz', 'aitor']    
                        },
                        
                        'luis' : {    'socialization' : 2.1,
                                      'activeness' : 400,
                                      'hobbies' : ['movies', 'sports'],
                                       'connections' : []    
                        },
                        
                        'juan' : {    'socialization' : 8,
                                      'activeness' : 100,
                                      'hobbies' : ['movies', 'sports'],
                                       'connections' : ['aritz', 'aitor']    
                        },
    
                    }
                    
    results = matchmaking(test_profiles)
    print results
                    
    
        
    
    