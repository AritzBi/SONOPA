# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:10:50 2015

@author: aitor
"""

 #{'pepito' : {
        #    'activeness' : 23.2,
        #    'socialization' :  12.1,
        #    'hobbies' : ['a', 'b'],
        #    'connections' : ['aitor', 'aritz'],}}

def _get_activeness_similarity(activeness1, activeness2):
    HA = 0
    LA = 0
    
    if activeness1 > activeness2:
        HA = activeness1
        LA = activeness2
    else:
        HA = activeness2
        LA = activeness1
    
    HA = HA * 1.0
    LA = LA * 1.0    
    SA = 1 - ((HA - LA) / HA)
    return SA

def _get_hobby_similarity(hobby_set1, hobby_set2):
    # jaccard
    SH = len(hobby_set1 & hobby_set2) * 1.0 / len(hobby_set1 | hobby_set2) * 1.0 
    return SH
    
def _get_connections_similarity(conns1, conns2):
    # jaccard
    SC = len(conns1 & conns2) * 1.0 / len(conns1 | conns2) * 1.0 
    return SC
    
def get_similarity(user1, user2):
    # Activeness similarity
    activeness1 = user1['activeness']
    activeness2 = user2['activeness']
    SA = _get_activeness_similarity(activeness1, activeness2)
    
    # Hobby similarity
    hobby_set1 = user1['hobbies']
    hobby_set2 = user2['hobbies']
    SH = _get_hobby_similarity(hobby_set1, hobby_set2)
    
    # Connection similarity
    conns1 = user1['connections']
    conns2 = user2['connections']
    SC =  _get_connections_similarity(conns1, conns2)
    
    S = (SA + SH + SC) / 3.0
    
    #print 'SA: %s, SH: %s, SC: %s, S: %s' % (SA, SH, SC, S)
    
    return S
    
    
        