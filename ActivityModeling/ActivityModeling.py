__author__ = 'AritzBi'
# Date management
import datetime
# Numerical computation
from pandas import to_datetime
from scipy.interpolate import UnivariateSpline
# Graphs
import networkx as nx

import random
import json
import copy
debug=False

class HMM:
	INF=float('inf')
	NEG_INF=float('-inf')
	def __init__(self,states=None, observations=None, init_matrix=None, trans_matrix=None, emit_matrix = None):
		self.st_list=None
		self.st_list_index=None
		self.ob_list=None
		self.ob_list_index=None
		self.init_matrix=None
		self.trans_matrix=None
		self.emit_matrix=None

		self.alpha_table=None
		self.beta_table=None
		self.xi_table=None
		self.gamma_table=None
		self.viterbi_table = None

		if(states is not None):
			self.set_states(states)
		if(observations is not None):
			self.set_observations(observations)
		if(init_matrix is not None):
			self.set_initial_matrix(init_matrix)
		if(trans_matrix is not None):
			self.set_transition_matrix(trans_matrix)
		if(emit_matrix is not None):
			self.set_emission_matrix(emit_matrix)
	def __build_internal_tables(self,ob_len):
		st_list_len=len(self.st_list)
		st_range=xrange(st_list_len)
		ob_range=xrange(ob_len)
		neg_inf = self.NEG_INF
		self.alpha_table = [[neg_inf for st in st_range] for t in xrange(ob_len + 1)]
		self.beta_table = [[neg_inf for st in st_range] for t in xrange(ob_len + 1)]
		self.xi_table = [[[neg_inf for st_j in st_range] for st_i in st_range] for ob in ob_range]
		self.gamma_table = [[neg_inf for st in st_range] for ob in ob_range]
		 # calculate __ln(x)
	def __ln(self, value):
		if (value == 0.0):
			return self.NEG_INF
		else:
			return math.log(value)
	def viterbi(self, ob_seq):
		#Number of possible states
		N=len(self.st_list)
		#Number of observations
		ob_seq_len=len(ob_seq)
		#initialize viterbi table's with NEG_INF [[-inf, -inf], [-inf, -inf], [-inf, -inf], [-inf, -inf]]
		viterbi_table = [[self.NEG_INF for st in xrange(N)] for t in xrange(ob_seq_len + 1)]
		#[[-inf, -inf], [-inf, -inf], [-inf, -inf]]
		bp_table = [[self.NEG_INF for st in xrange(N)] for t in xrange(ob_seq_len)]
		#The sequence of observations in number [0, 0, 2]
		ob_seq_int = [self.ob_list_index[ob] for ob in ob_seq]
		# initialize viterbi table's first entry [[0.6, 0.4], [-inf, -inf], [-inf, -inf], [-inf, -inf]]
		for i in xrange(N):
			viterbi_table[0][i] = self.init_matrix[i]
		for t in xrange(1, ob_seq_len + 1): # loop through time
			#printea los identificadores de las observaciones 0 0 2 
			ot = ob_seq_int[t - 1]
			for st_j in xrange(N): # for each state
				viterbi_t_j = self.NEG_INF
				curr_best_st = None
				for st_i in xrange(N):
					log_sum = viterbi_table[t - 1][st_i] + self.trans_matrix[st_i][st_j] + self.emit_matrix[st_j][ot]
					if (log_sum > viterbi_t_j):
						viterbi_t_j = log_sum
						curr_best_st = st_i
				viterbi_table[t][st_j] = viterbi_t_j
				#print viterbi_table
				bp_table[t - 1][st_j] = curr_best_st
		# perform the viterbi back-trace
		t = len(bp_table) - 1
		if (t < 0):
			return None
		states_seq = [0] * ob_seq_len
		curr_state=0
		for st in xrange(N):
			if (bp_table[-1][st] > bp_table[-1][curr_state]):
				curr_state = st
		for t in xrange(ob_seq_len - 1, -1, -1):
			if (curr_state is None):
				return None
			states_seq[t]=self.st_list[curr_state]
			curr_state=bp_table[t][curr_state]
		return states_seq
	# set the list of states
	def set_states(self, st_seq):
		self.st_list = copy.copy(st_seq)
		# build the index automatically
		self.st_list_index = dict()
		for i in xrange(len(st_seq)):
			self.st_list_index[st_seq[i]] = i
	def set_observations(self,ob_seq):
		self.ob_list=copy.copy(ob_seq)
		#build the index automatically
		self.ob_list_index=dict()
		for i in xrange(len(ob_seq)):
			self.ob_list_index[ob_seq[i]]=i
	def set_initial(self,st,prob):
		self.init_matrix[self.st_list_index[st]] = prob
	def set_initial_matrix(self, Pi_matrix):
		ln_0 = self.__ln(0.0)
		N = len(self.st_list)
		self.init_matrix = [ln_0 for st in xrange(N)]
		for st in Pi_matrix:
			self.init_matrix[self.st_list_index[st]] = Pi_matrix[st]
	# set the transition probability matrix, P(state[i] -> state[j]) = A[i][j]
	def set_transition_matrix(self, A_matrix):
		ln_0 = self.__ln(0.0)
		N = len(self.st_list)
		self.trans_matrix = [[ln_0 for st_i in xrange(N)]  for st_j in xrange(N)]
		#self.trans_matrix_copy = [[ln_0 for st_i in xrange(N)]  for st_j in xrange(N)]
		for st_i in A_matrix:
			for st_j in A_matrix[st_i]:
				self.trans_matrix[self.st_list_index[st_i]][self.st_list_index[st_j]] = A_matrix[st_i][st_j]

	#set the emission probability matrix
	def set_emission_matrix(self,B_matrix):
		N=len(self.st_list)
		ob_list_len=len(self.ob_list)
		ln_0=self.__ln(0.0)
		self.emit_matrix = [[ln_0 for st in xrange(ob_list_len)] for ob in xrange(N)]
		self.emit_matrix_copy = [[ln_0 for st in xrange(ob_list_len)] for ob in xrange(N)]
		for st in B_matrix:
			for ob in B_matrix[st]:
				self.emit_matrix[self.st_list_index[st]][self.ob_list_index[ob]] = B_matrix[st][ob]


class HSMM:



states= ('Rainy','Sunny')
observations=('walk','shop','clean')
test_observations=('walk','walk','clean')
start_probability = {'Rainy': 0.6, 'Sunny': 0.4}
transition_probability = {
	'Rainy' : {'Rainy': 0.7, 'Sunny': 0.3},
	'Sunny' : {'Rainy': 0.4, 'Sunny': 0.6},
	}
 
emission_probability = {
	'Rainy' : {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
	'Sunny' : {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
	}
hmm=HMM(states,observations,start_probability,transition_probability,emission_probability)
print hmm.viterbi(test_observations)