# -*- coding: utf-8 -*-
"""
Copyright (c) 2015 Aitor Almeida, Aritz Bilbao

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

@author: "Aitor Almeida, Aritz Bilbao"
@contact: aitor.almeida@deusto.es, aritzbilbao@deusto.es
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
    print "Calculating the minimun socialization level for the user",current_user
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

    
