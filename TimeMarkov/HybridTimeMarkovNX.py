__author__ = 'hasier'

# Date management
import datetime

# Numerical computation
from pandas import to_datetime
from scipy.interpolate import UnivariateSpline

# Graphs
import networkx as nx
import community

import random

import json


debug = False


class Transition:
    """
    Represents that an activity has been made after another one in the model.

    It contains different attributes to tune the different time ranges in which the activities have dependencies.
    """

    nSlots = 24 * 4
    """Represents the number of time slots in each slot of a day (and therefore their duration).
    This helps tuning the moments in which activities happen. This way, the activities
    can be predicted (in this case) within 15 minutes difference. Depends on _get_position"""

    def __init__(self):
        self.prob = 0.0
        self.count = 0.0
        self._slots = [0.0 for _ in range(Transition.nSlots)]
        self._slotsProb = [0.0 for _ in range(Transition.nSlots)]
        self._regression = None

    @staticmethod
    def _get_position(diff):
        """
        Returns the time slot of the provided time diff
        """
        return diff.seconds / (3600.0 / 4.0)

    def add_occurrence(self, diff):
        """
        Adds a new occurrence to this transition given a time diff from the previous activity.
        """
        self.count += 1
        if diff is not None:
            self._slots[int(Transition._get_position(diff))] += 1
        else:
            self._slots[0] += 1

    def calculate_prob(self, total):
        """
        Calculates the current probability of this transition
        """
        if total == 0.0:
            self.prob = 0.0
        else:
            self.prob = self.count / total
            line = sum(self._slots)
            if line != 0:
                for i in range(len(self._slots)):
                    self._slotsProb[i] = self._slots[i] / line
                self._regression = UnivariateSpline(range(Transition.nSlots), self._slotsProb)

    def get_prob(self, time_diff):
        """
        Gets the probability of this transition given a time diff
        """
        if self._regression is None:
            return 0.0
        else:
            return self._regression(self._get_position(time_diff))

    def __repr__(self):
        return str(self.prob)


class Markov:

    nStates = 5
    """Represents the number of day slots into which a day is divided. Depends on get_day_slot"""

    @staticmethod
    def get_day_slot(time):
        """Returns the slot to which the given datetime belongs"""
        if time.hour >= 23 or time.hour < 7:
            return str(0)
        elif 7 <= time.hour < 12:
            return str(1)
        elif 12 <= time.hour < 16:
            return str(2)
        elif 16 <= time.hour < 20:
            return str(3)
        elif 20 <= time.hour < 23:
            return str(4)

    def __init__(self, sequence=None):
        """
        Initializes a new Markov activity model.

        If sequence is given, the chain is initialized with its contents. It must follow this format:
        [[activity_name1, datetime1], [activity_name2, datetime2], ...]
        """
        self._graph = nx.DiGraph()
        self._last_training_time = None
        self._last_time = None
        self._last_activity = None
        if not sequence is None:
            self._initialize(sequence)
        self._is_training = True

    def set_training(self, training):
        """Enables or disables the training mode"""
        self._is_training = training

    def _initialize(self, sequence):
        """Initializes the chain with the given sequence"""
        self._init_nodes(sequence)

        for i in range(1, len(sequence)):
            u = sequence[i - 1][0] + Markov.get_day_slot(sequence[i - 1][1])
            v = sequence[i][0] + Markov.get_day_slot(sequence[i][1])

            t2 = sequence[i][1]
            diff = None
            if self._last_training_time is not None:
                diff = t2 - self._last_training_time
            self._last_training_time = t2

            if not self._graph.has_edge(u, v):
                self._graph.add_edge(u, v)
                self._graph[u][v]['transition'] = Transition()
            self._graph[u][v]['transition'].add_occurrence(diff)

        for node in self._graph.nodes():
            self._calculate_node(node)

    def _init_nodes(self, sequence):
        """Initializes the chain nodes with the activity names in the sequence"""
        for element in sequence:
            self._init_node(element[0])

    def _init_node(self, element):
        """
        Given an activity name, if its node does not exist in the model, creates the necessary ones and inserts them
        """
        slot = element + str(0)
        if not slot in self._graph:
            for i in range(Markov.nStates):
                self._graph.add_node(element + str(i))

    def _calculate_node(self, node):
        """Recalculates the weights and probabilities of the given activity name and its dependents"""
        line = 0.0
        for key in self._graph[node].keys():
            line += self._graph[node][key]['transition'].count
        for j in self._graph.nodes():
            if self._graph.has_edge(node, j):
                self._graph[node][j]['transition'].calculate_prob(line)

    def init_lasts(self, last_activity, last_time):
        """
        For a cold start, initializes the chain's last activity and its time
        to be able to calculate the next new activity probabilities
        """
        self._last_activity = last_activity + Markov.get_day_slot(last_time)
        self._last_time = last_time

    def new_event(self, time_diff, activity):
        """Introduces a new activity into the chain with the given diff from the previous activity"""
        if self._is_training:
            self._init_node(activity)

        if self._last_time is None:
            if debug:
                self._last_time = datetime.datetime(2008, 6, 29, 13, 06, 22) - time_diff
            else:
                self._last_time = datetime.datetime.today() - time_diff
        elif debug:
            self._last_time = datetime.datetime(2008, 6, 29, 23, 40, 22)
        activity += Markov.get_day_slot(self._last_time)
        self._last_time = self._last_time + time_diff

        if self._last_activity is not None:
            if not self._graph.has_edge(self._last_activity, activity):
                self._graph.add_edge(self._last_activity, activity)
                self._graph[self._last_activity][activity]['transition'] = Transition()
            self._graph[self._last_activity][activity]['transition'].add_occurrence(time_diff)
            self._calculate_node(activity)
        self._last_activity = activity

    def get_prob(self, previous, previous_time, time_diff):
        """
        Returns the different probabilities for the activities in the chain
        given a previous activity on a given time and after a time diff
        """
        probs = []
        previous += Markov.get_day_slot(previous_time)

        probs.append("if '" + previous + "' then ")
        for item in self._graph[previous].keys():
            probs.append(item + ' with prob ' + str(self._graph[previous][item]['transition'].get_prob(time_diff)))

        return probs

    def get_last_prob(self, time_diff):
        """
        Returns the different probabilities for the activities in the chain given a time diff from the last activity
        """
        probs = []
        if self._last_time is None:
            if debug:
                self._last_time = datetime.datetime(2008, 6, 29, 13, 06, 22) - time_diff
            else:
                self._last_time = datetime.datetime.today() - time_diff
        elif debug:
            self._last_time = datetime.datetime(2008, 6, 29, 23, 40, 22)
        self._last_time = self._last_time + time_diff

        probs.append("if '" + self._last_activity + "' then ")
        for item in self._graph[self._last_activity].keys():
            probs.append(item + ' with prob '
                         + str(self._graph[self._last_activity][item]['transition'].get_prob(time_diff)))

        return probs

    def export_gexf(self):
        """Exports the current chain to gexf to be able to visualize it"""
        # Make local copy of graph and transform Transition objects to string
        # to avoid gexf file write crash in xml type inference
        graph = self._graph.copy()
        for node1 in graph:
            for node2 in graph:
                if node2 in graph[node1] and 'transition' in graph[node1][node2]:
                    graph[node1][node2]['transition'] = str(graph[node1][node2]['transition'])

        #calculate pagerank to use it as node size
        pagerank = nx.pagerank(graph)

        for node in graph:
            graph.node[node]['pagerank'] = pagerank[node]

        graph_undirected = graph.to_undirected()

        partitions = community.best_partition(graph_undirected)
        colors = {}
        for member, c in partitions.items():
            if not c in colors:
                r = random.randrange(256)
                g = random.randrange(256)
                b = random.randrange(256)
                colors[c] = (r, g, b)

            graph.node[member]["viz"] = {'color': {'r': colors[c][0],
                                                   'g': colors[c][1],
                                                   'b': colors[c][2],
                                                   },
                                         'size': 5 * graph.node[member]['pagerank']
                                         }

        nx.write_gexf(graph, './output/test.gexf')

    def __repr__(self):
        return str(self._graph.edges(data=True))

    def export_json(self):
        """Serializes the chain to JSON format"""
        def default(o):
            if isinstance(o, Transition):
                d = o.__dict__.copy()
                d.pop('_regression', None)
                return json.dumps(d)
            return json.JSONEncoder.default(json.JSONEncoder(), o)
        return json.dumps(self._graph.edges(data=True), default=default)

    def import_json(self, json_str_graph):
        """Imports into the chain the provided JSON string representing a Markov object"""
        obj = json.loads(json_str_graph)
        for o in obj:
            self._init_node(o[0][:len(o[0]) - 1])
            self._init_node(o[1][:len(o[1]) - 1])
            self._graph.add_edge(o[0], o[1])
            t = Transition()
            t.__dict__.update(json.loads(o[2]['transition']))
            self._graph[o[0]][o[1]]['transition'] = t


if __name__ == '__main__':
    global debug
    debug = True
    f = open('./data/tulum2010')
    ao = []
    for file_line in f:
        split = file_line.split('\t')
        if len(split) >= 5 and split[4].strip() != "":
            ao.append([split[0], split[1], split[4].rstrip()])

    a = []

    for x in xrange(len(ao)):
        a.append(ao[x][0] + ' ' + ao[x][1])

    dates = to_datetime(a, dayfirst=False)

    seq = []

    for x in xrange(len(ao)):
        seq.append([ao[x][2], dates[x]])

    cl = Markov(seq)
    print cl
    print
    # print str(cl.get_last_prob(datetime.timedelta(0, 7200), 'R1_Sleeping_in_Bed'))  # Personal_Hygiene
    cl.new_event(datetime.timedelta(0, 7200), 'R1_Sleeping_in_Bed')
    print str(cl.get_last_prob(datetime.timedelta(0, 7200)))  # Personal_Hygiene
    print
    # print str(cl.get_last_prob(datetime.timedelta(0, 60), 'Meal_Preparation'))  # Meal_Preparation
    cl.new_event(datetime.timedelta(0, 60), 'Meal_Preparation')
    print str(cl.get_last_prob(datetime.timedelta(0, 60)))  # Meal_Preparation
    print
    cl.export_gexf()
    print 'Export done'
    j = cl.export_json()
    # print j
    print 'JSON done'
    cl2 = Markov()
    cl2.import_json(j)
    print cl2
    print 'JSON import done'