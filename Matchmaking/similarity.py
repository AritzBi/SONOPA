# -*- coding: utf-8 -*-
"""
Copyright (c) 2015 Aitor Almeida

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

@author: "Aitor Almeida"
@contact: aitor.almeida@deusto.es
"""

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
    
    try:
        SA = 1 - ((HA - LA) / HA)
    except ZeroDivisionError:
        SA = 0
        
    return SA

def _get_hobby_similarity(hobby_set1, hobby_set2):
    # jaccard
    try:
        SH = len(hobby_set1 & hobby_set2) * 1.0 / len(hobby_set1 | hobby_set2) * 1.0 
    except ZeroDivisionError:
        SH = 0
    return SH
    
def _get_connections_similarity(conns1, conns2):
    # jaccard
    try:
        SC = len(conns1 & conns2) * 1.0 / len(conns1 | conns2) * 1.0 
    except ZeroDivisionError:
        SC = 0
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
    
    
        
