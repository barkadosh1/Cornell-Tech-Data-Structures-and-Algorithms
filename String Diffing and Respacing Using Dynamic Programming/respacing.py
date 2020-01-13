# TODO: Bar Kadosh, bk497
# TODO: Ben Kadosh, bk499

# DO NOT CHANGE THIS CLASS
class RespaceTableCell:
    def __init__(self, value, index):
        self.value = value
        self.index = index
        self.validate()

    # This function allows Python to print a representation of a RespaceTableCell
    def __repr__(self):
        return "(%s,%s)"%(str(self.value), str(self.index))

    # Ensure everything stored is the right type and size
    def validate(self):
        assert(type(self.value) == bool), "Values in the respacing table should be booleans."
        assert(self.index == None or type(self.index) == int), "Indices in the respacing table should be None or int"

# Inputs: the dynamic programming table, indices i, j into the dynamic programming table, the string being respaced, and an "is_word" function.
# Returns a RespaceTableCell to put at position (i,j)
def fill_cell(T, i, j, string, is_word):

    #here we want to check if the string from i to j is in fact a word in the dictionary
    #or is a partition of other words in the string and insert a bool value accordingly
    #and if partitioned the partition index

    #calculate the length of the string in the given cell
    length = j - i + 1

    #set the initial final partition index to -1 (convention we set)
    final_partition_index = -1

    #check if the string being tested
    bool_val = is_word(string[i:j+1])

    #if the bool val is false and the string tested is larger than 1 check if it can be partitioned
    #such that there are two strings within it that are words in the dictionary
    #o(N) complexity
    #use a for loop to move the partition index from 1 to the end of the substring being analyzed
    #if partitioned used the dynammic programming table to calculate previously calculated words
    if bool_val == False and length > 1:
        for partition_index in range(1,length):

            if T.get(i, j-(length - partition_index)).value == True and T.get(i + partition_index, j).value  == True:
                final_partition_index = partition_index

        #if final partition index was set, set bool val to true
        if final_partition_index > -1:
            bool_val = True

    #return the bool val and partition index
    return RespaceTableCell(bool_val, final_partition_index)

# Inputs: N, the size of the list being respaced
# Outputs: a list of (i,j) tuples indicating the order in which the table should be filled.
def cell_ordering(N):


    #here we want to increment for the top half triangle of the matrix and start with indices for
    #1 letter in the string, then 2 letters in the string,
    #and increment until we have analyzed all possible letter counts from 1 to length of the entire string

    #create an empty array to store the cell ordering and use a nested for loop to
    #append the relevant tuples for order
    order = []
    for j in range(N):
        for i in range(N,-1,-1):
            if j>= i:
                order.append((i,j))
    return order

# Input: a filled dynamic programming table.
# (See instructions.pdf for more on the dynamic programming skeleton)
# Return the respaced string, or None if there is no respacing.
def respace_from_table(s, table):

    #create an empty string to store the respaced string of s
    respaced = ''

    #calculate the length of s for # of columns
    j = len(s)-1

    #for this process, we want to start at rightmost column of the table in row 0
    #we will then work down the row and look for the first True value by accessing table.get().value
    #we do this and move along the top half triangle of the table as needed.
    #when we hit a true we will adjust the indices accordingly
    #if we iterate through a whole column and have not found a true, we know there is at least one character
    #that is not a part of any word in the string and therefore, we return None

    #iterate while our column still has room to move right
    while(j >= 0):

        #set i to 0 and use a while loop to iterate and increment from 0 to the bottom most cell in the
        #top half triangle of the table
        #if we make it to the bottom return None
        i = 0
        while(i < len(s)):

            #fix the parameters of the loops to the top half triangle of the table
            if j>= i:

                #as we iterate down the rows check in each cell if the value is true
                if table.get(i,j).value == True:

                    #if true get the partition index from that cell
                    partition = table.get(i,j).index

                    #check for words that are not part of a partition of wordlist
                    #determine if respace is empty or not to know if to add a space or not
                    #if we find a non partitioned word and i is greater than 0 everything to the right
                    #is a string that cannot be partitioned into words in the dictionary so we return None
                    #set i and j to negative indices to end the while loops
                    if partition == -1:
                        if respaced == '':
                            respaced = s[i:j+1]
                            if i > 0 :
                                return None

                            j = -2
                            i = -1
                        else:
                            respaced = s[i:j+1] + ' ' + respaced
                            if i > 0 :
                                return None

                            j = -2
                            i = -1

                    #if the word is partitioned and comprised of other words follow similar proceduce to above
                    #check if the respace string is empty or not to know whether to add a space
                    #add the characters to the right of the partition
                    #reset j to shift it left past the set of characters we add to respaced
                    #reset i to -1 will increment to 0 which is the first row in the new column we set with j
                    else:
                        if respaced == '':
                            respaced =  s[i+partition:j+1]
                            j = i + partition -1
                            i = -1
                        else:
                            respaced =  s[i+partition:j+1] + ' ' + respaced
                            j = i + partition - 1
                            i = -1

            #if we reach the bottom of the row we did not find a true and we return None
            if i == j:
                return None

            #increment i
            i+=1

    #return respaced
    return respaced



if __name__ == "__main__":
    # Example usage.
    from dynamic_programming import DynamicProgramTable
    s = "itwasthebestoftimes"
    wordlist = ["of", "it", "the", "best", "times", "was"]


    D = DynamicProgramTable(len(s) + 1, len(s) + 1, cell_ordering(len(s)), fill_cell)
    D.fill(string=s, is_word=lambda w:w in wordlist)
    print respace_from_table(s, D)
