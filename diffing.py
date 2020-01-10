# TODO: Bar Kadosh, bk497
# TODO: Ben Kadosh, bk499

import dynamic_programming

# initializing a global variable that will keep track of whether each cell's
# previous cell is the diagonal (by storing 0), the left (by storing 1),
# or up (by storing 2)
movement_tracker = []

# DO NOT CHANGE THIS CLASS
class DiffingCell:
    def __init__(self, s_char, t_char, cost):
        self.cost = cost
        self.s_char = s_char
        self.t_char = t_char
        self.validate()

    # Helper function so Python can print out objects of this type.
    def __repr__(self):
        return "(%d,%s,%s)"%(self.cost, self.s_char, self.t_char)

    # Ensure everything stored is the right type and size
    def validate(self):
        assert(type(self.cost) == int), "cost should be an integer"
        assert(type(self.s_char) == str), "s_char should be a string"
        assert(type(self.t_char) == str), "t_char should be a string"
        assert(len(self.s_char) == 1), "s_char should be length 1"
        assert(len(self.t_char) == 1), "t_char should be length 1"

# Input: a dynamic programming table,  cell index i and j, the input strings s and t, and a cost function cost.
# Should return a DiffingCell which we will place at (i,j) for you.
def fill_cell(table, i, j, s, t, cost):
    # add 0 to the table for '-', '-' and arbitrarily add 0 to the movement_tracker
    # array (we will not really need to access it)
    if i == 0 and j == 0:
        movement_tracker.append(0)
        return DiffingCell('-', '-' , 0)
    # add 1 to the table for values on the first row of the movement_tracker
    # array. On this row, the only previous value could be to the left
    # Calculate and add the cost of the previous cell to the current cell
    elif i == 0:
        if j == 1:
            movement_tracker.append(1)
            return DiffingCell( '-', t[j-1] , cost('-', t[j-1]))
        else:
            movement_tracker.append(1)
            prior_cost = table.get(i,j-1).cost
            return DiffingCell( '-', t[j-1] , cost('-', t[j-1])+ prior_cost)
    # add 2 to the table for values on the first column of the movement_tracker
    # array. On this cokumn, the only previous value could be above
    # Calculate and add the cost of the previous cell above to the current cell
    elif j == 0 :
        if i == 1:
            movement_tracker.append(2)
            return DiffingCell(s[i-1], '-', cost(s[i-1], '-'))
        else:
            movement_tracker.append(1)
            prior_cost = table.get(i-1,j).cost
            return DiffingCell(s[i-1], '-', cost(s[i-1], '-')+ prior_cost)
    # calculate the 3 possible costs: adding the diagonal cost to the cost of the
    # two letters in the cell, adding the left cost to the cost of a dash and
    # the t-letter, and adding the up cost to the cost of a dash and the s-letter.
    # take the minimum calculation to determine which one will be considered
    # the 'previous' cell and append a 0, 1, or 2 to the movement_tracker array
    # accordingly
    else:
        diagonal = table.get(i-1,j-1).cost + cost(s[i-1], t[j-1])
        left = table.get(i,j-1).cost + cost('-', t[j-1])
        up = table.get(i-1,j).cost + cost(s[i-1], '-')

        cost_val = min(diagonal, left, up)

        if cost_val == diagonal: movement_tracker.append(0)
        elif cost_val == left: movement_tracker.append(1)
        else: movement_tracker.append(2)

        return DiffingCell(s[i-1], t[j-1], cost_val)



# Input: n and m, represents the sizes of s and t respectively.
# Should return a list of (i,j) tuples, in the order you would like fill_cell to be called
def cell_ordering(n,m):
    order = []
    for i in range(n+1):
        for j in range(m+1):
            order.append((i,j))
    return order

# Returns a size-3 tuple (cost, align_s, align_t).
# cost is an integer cost.
# align_s and align_t are strings of the same length demonstrating the alignment.
# See instructions.pdf for more information on align_s and align_t.
def diff_from_table(s, t, table):
    # defining different lengths and index pointers we will use in our function
    # i and j are the indices of our table, while s_index and t_index are index
    # pointers that point to the current letter in s and t, respectively
    len_s = len(s) + 1
    len_t = len(t) + 1
    i = len(s)
    j = len(t)
    s_index = len(s) - 1
    t_index = len(t) - 1
    # initialize our optimal return strings to empty strings
    align_s = ''
    align_t = ''
    # length of our array that stores the 'prev' value for each cell (wether
    # the previous is the diagonal, the left, or the above cell)
    # initializing the 'prev' value for the bottom right corner at (i,j)
    prev_index = len(movement_tracker) -1
    prev_val = movement_tracker[prev_index]

    # the cost value in the bottom right of our table represents the optimal
    # cost of the optimal alignment (at indices (i,j))
    return_cost = table.get(i,j).cost

    # the while loop continues running so long as we have not reached the upper
    # left corner of our table (have fully iterated through the reconstructed
    # path)
    while (i > 0 or j > 0):
        # once all values in s have been accepted, dashes are added to align_s
        # for the rest of the process
        if s_index < 0:
            while (t_index >= 0):
                align_s = '-' + align_s
                align_t = t[t_index] + align_t
                t_index -= 1
            j = 0
            i = 0
        # once all values in t have been accepted, dashes are added to align_s
        # for the rest of the process
        elif t_index < 0:
            while (s_index >= 0):
                align_t = '-' + align_t
                align_s = s[s_index] + align_s
                s_index -= 1
            i = 0
            j = 0
        # if both s and t still have characters available, we look at the prev
        # val. If it is 0 (diagonal), we accept both the letters from s and t
        # into align_s and align_t. If it is 1 (left), we accept a dash into
        # align_s and the t-letter into t_align. If it is 2 (up), we accept
        # a dash into align_t and the s-letter into s_align
        else:
            if prev_val == 0:
                align_s = s[s_index] + align_s
                align_t = t[t_index] + align_t
                i -= 1
                j -= 1
                s_index -= 1
                t_index -= 1

                prev_index = prev_index - len_t - 1
                prev_val = movement_tracker[prev_index]
            elif prev_val == 1:
                align_s = '-' + align_s
                align_t = t[t_index] + align_t
                t_index -= 1
                j -= 1

                prev_index = prev_index - 1
                prev_val = movement_tracker[prev_index]
            else:
                align_t = '-' + align_t
                align_s = s[s_index] + align_s
                s_index -= 1
                i -= 1

                prev_index = prev_index - len_t
                prev_val = movement_tracker[prev_index]

    return (return_cost, align_s, align_t)

# Example usage
if __name__ == "__main__":
    # Example cost function from instructions.pdf
    def costfunc(s_char, t_char):
        if s_char == t_char: return 0
        if s_char == 'a':
            if t_char == 'b': return 5
            if t_char == 'c': return 3
            if t_char == '-': return 2
        if s_char == 'b':
            if t_char == 'a': return 1
            if t_char == 'c': return 4
            if t_char == '-': return 2
        if s_char == 'c':
            if t_char == 'a': return 5
            if t_char == 'b': return 5
            if t_char == '-': return 1
        if s_char == '-':
            if t_char == 'a': return 3
            if t_char == 'b': return 3
            if t_char == 'c': return 3

    # example strings for testing
    s = "bababacaabacbacbacbbbca"
    t = "accbbbaaaaaa"
    # build the dynamic programming table and fill it
    D = dynamic_programming.DynamicProgramTable(len(s) + 1, len(t) + 1, cell_ordering(len(s), len(t)), fill_cell)
    D.fill(s = s, t = t, cost=costfunc)
    # retrieve and print the minimum cost and optimal align_s and align_t
    # values using diff_from_table
    (cost, align_s, align_t) = diff_from_table(s,t, D)
    print align_s
    print align_t
    print "cost was %d"%cost
