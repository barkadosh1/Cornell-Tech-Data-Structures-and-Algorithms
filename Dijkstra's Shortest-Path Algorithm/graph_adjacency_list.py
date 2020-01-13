# TODO: Bar Kadosh, bk497
# TODO: Ben Kadosh, bk499
 
# Please see instructions.txt for the description of this problem.
from exceptions import NotImplementedError

# An implementation of a weighted, directed graph as an adjacency list. This
# means that it's represented as a map from each node to a list of it's
# respective adjacent nodes.

class Graph:
  def __init__(self):
    # DO NOT EDIT THIS CONSTRUCTOR
    self.graph = {}

  def add_edge(self, node1, node2, weight):
    # Adds a directed edge from `node1` to `node2` to the graph with weight defined by `weight`.

    # if the key currently doesn't have a value, assign it the value of a tuple
    # of the second node in the edge and the weight of the edge
    if node1 not in self.graph.keys():
        self.graph[node1] = [(node2, weight)]
    # otherwise,take the current value and add a tuple of the current edge's
    # second node and the weight of that edge
    else:
        new_value = self.graph[node1]
        new_value.append((node2, weight))
        self.graph[node1] = new_value

  def has_edge(self, node1, node2):
    # Returns whether the graph contains an edge from `node1` to `node2`.
    # DO NOT EDIT THIS METHOD
    if node1 not in self.graph:
      return False
    return node2 in [x for (x,i) in self.graph[node1]]

  def get_neighbors(self, node):
    # Returns the neighbors of `node` as a list of tuples [(x, y), ...] where
    # `x` is the neighbor node, and `y` is the weight of the edge from `node`
    # to `x`.
    return self.graph[node]
