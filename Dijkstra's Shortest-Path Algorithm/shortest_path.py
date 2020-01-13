# TODO: Bar Kadosh, bk497
# TODO: Ben Kadosh, bk499
 
# Please see instructions.txt for the description of this problem.
from exceptions import NotImplementedError

def shortest_path(graph, source, target):
    queue = [] # queue of potential node and distance values
    visited = [] # keep track of examined nodes
    path = {} # empty dictionary to trace the optimal path

    # add the source node with a weight of 0 to the queue
    current_node = source
    current_value = 0
    queue.append((current_node, current_value))

    # just a counter for what iteration in the while loop we are in
    iter = 0

    #continue traversing the graph until we reach/examine target
    while (current_node != target):
        #get the neighbors of the current node
        neighbors_list = graph.get_neighbors(current_node)

        # if this is the first iteration through the while loop, make the queue
        # empty after examining the initial neighbors
        if queue[0][1] == 0:
            queue = []

        # iterate through each neighbor
        for neighbor in neighbors_list:
            node_val = neighbor[0]
            neighbor_weight_val = neighbor[1]
            current_weight_val = current_value

            # so long as we haven't examined this node, we add it to the queue
            # with a weight value that is the sum of its edge weight and the
            # weight of the path up until the edge
            if node_val not in visited:
                queue.append((node_val, neighbor_weight_val + current_weight_val))

                # if a path has not been added for this node, we add the path to
                # the previous node and append the previous node to the path
                # if it is the first set of neighbor nodes, we just add the
                # start node as the path
                # we also want it to follow this if statement if we are in the
                # first iteration of this while loop
                # includes a try except to avoid an error with checking weights
                # for a path with no current weight
                if node_val not in path.keys() or iter == 0:
                    if current_node not in path.keys():
                        try:
                            if (neighbor_weight_val + current_weight_val) < path[node_val][1]:
                                path[node_val] = ([current_node], neighbor_weight_val + current_weight_val)
                        except:
                            path[node_val] = ([current_node], neighbor_weight_val + current_weight_val)
                    else:
                        new_path = path[current_node][0][:]
                        new_path.append(current_node)
                        path[node_val] = (new_path, neighbor_weight_val + current_weight_val)
                # if a path has beeen added, we only update the path and weight
                # if the weight of the new path we are examining is less than
                # the weight of the path currently stored
                else:
                    if (neighbor_weight_val + current_weight_val) < path[node_val][1]:
                        new_path = path[current_node][0][:]
                        new_path.append(current_node)
                        path[node_val] = (new_path, neighbor_weight_val + current_weight_val)

        # add the current node to visited if it is not already in there
        if current_node not in visited:
            visited.append(current_node)

        # initializing values for the next chunk of code
        min = float("inf")
        index = 0
        count = 0

        # find the node in the queue with the smallest current path weight value
        # so that the the node with the minimum weight must not be in visited
        for node_and_weight in queue:
            current_node = node_and_weight[0]
            current_weight = node_and_weight[1]
            if current_weight < min and current_node not in visited:
                min = current_weight
                index = count
            count += 1

        # given our calculation above, we store the current node with the
        # smallest weight distance
        # we then set this node to None and create a copy of our queue without
        # the node that we just set to None as it is no longer a valid point
        # in our queue
        current_node = queue[index][0]
        current_value = queue[index][1]
        queue[index] = None
        queue_copy = []
        for node_and_weight in queue:
            if node_and_weight != None:
                queue_copy.append(node_and_weight)
        queue = queue_copy

        iter += 1

    # extract the final path from our path dictionary and return it and its
    # minimum distance
    final_path = path[current_node][0]
    final_path.append(current_node)
    return (final_path, current_value)
