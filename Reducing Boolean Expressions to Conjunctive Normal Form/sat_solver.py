# TODO: Bar Kadosh, bk497
# TODO: Ben Kadosh, bk499

# import the needed libraries/files
from helpers import *
from cnf_sat_solver import dpll

# DO NOT CHANGE SAT_solver
# Convert to Conjunctive Normal Form (CNF)
"""
>>> to_cnf_gadget('~(B | C)')
(~B & ~C)
"""
def to_cnf_gadget(s):
    s = expr(s)
    if isinstance(s, str):
        s = expr(s)
    step1 = parse_iff_implies(s)  # Steps 1
    step2 = deMorgansLaw(step1)  # Step 2
    return distibutiveLaw(step2)  # Step 3

# ______________________________________________________________________________
# STEP1: if s has IFF or IMPLIES, parse them

# TODO: depending on whether the operator contains IMPLIES('==>') or IFF('<=>'),
# Change them into equivalent form with only &, |, and ~ as logical operators
# The return value should be an Expression (e.g. ~a | b )

# Hint: you may use the expr() helper function to help you parse a string into an Expr
# you may also use the is_symbol() helper function to determine if you have encountered a propositional symbol
def parse_iff_implies(s):
    # assign the operator and arguments
    op = s.op
    args = s.args

    # case where the argument is just a letter, because op will only return
    # the letter as the op when no other possible op is present (&, |, etc.)
    if is_symbol(op) == True:
        return s

    # case where the operator is not. Return the not operator plus the recursive
    # return value of the rest of the expression
    if op == "~":
        return expr(op + str(parse_iff_implies(expr(args[0]))))

    # case where the operator is <=>. It alters the operator of the expression
    # to & and takes the 2 arguments (A and B) so that the new arguments are
    # (A --> B) and (B --> A), where A and B represent the two arguments, whatever
    # they may be. It calls the recursive function on this altered expression
    if op == "<=>":
        one = str(args[0])
        two = str(args[1])
        new_one = expr(one+'==>'+two)
        new_two = expr(two+'==>'+one)
        s.op = '&'
        s.args = (new_one, new_two)
        return parse_iff_implies(s)

    # case where op is ==>. It alters the operator to be | and adds a not sign
    # to the first argument. If this altered expression no longer contains
    # ==> or <=> symbols, we simply return the expression. If it still does, we
    # call the recursive function on this altered expression
    if op == "==>":
        one = str(args[0])
        two = args[1]
        new_one = expr('~' + one)
        s.op = '|'
        s.args = (new_one, two)
        new_string = str(s)
        if "==>" not in new_string and "<=>" not in new_string:
            return s
        else:
            return parse_iff_implies(s)

    # case where the operator is something else (& or |). If ==> and <==> symbols
    # also aren't present in the arguments of the expression, we can just return
    # the expression as it is. If they are present in the arguments, however,
    # we return the recursive return of the first argument added to the operator
    # (& or | in this case) and add it to what we return from the recursive call
    # on the second argument
    if op != "==>" and op != "<=>":
        if "==>" not in str(args[0]) and "<=>" not in str(args[0]) and "==>" not in str(args[1]) and "<=>" not in str(args[1]):
            return s
        else:
            new_s = str(parse_iff_implies(args[0])) + op + str(parse_iff_implies(expr(args[1])))
            s = expr(new_s)
            return s



# ______________________________________________________________________________
# STEP2: if there is NOT(~), move it inside, change the operations accordingly.

""" Example:
>>> deMorgansLaw(~(A | B))
(~A & ~B)
"""

# TODO: recursively apply deMorgansLaw if you encounter a negation('~')
# The return value should be an Expression (e.g. ~a | b )

# Hint: you may use the associate() helper function to help you flatten the expression
# you may also use the is_symbol() helper function to determine if you have encountered a propositional symbol
def deMorgansLaw(s):
    # assign the operator and arguments
    s = expr(s)
    op = s.op
    args = s.args

    # when the operator is ~, follow this path of code
    if op == "~":
        # assign the sub-operator and sub-arguments for the argument attached
        # to the parent ~ operator
        sub = args[0]
        sub_op = sub.op
        sub_args = sub.args

        # return the symbol if it is the suboperator, as this means there is no
        # other operator present
        if is_symbol(sub_op) == True:
            return s

        # if the sub operator is also a ~ operator, then we return the sub-sub
        # argument without the two ~ symbols as they should cancel each other
        if sub_op == "~":
            return deMorgansLaw(sub_args[0])

        # case where the sub operator is an & or an |
        if sub_op == "&" or sub_op == "|":
            # If it is an &, we change it to an |, and vice versa
            if sub_op == "&":
                sub.op = "|"
            else:
                sub.op = "&"

            # sub arguments
            one = str(sub_args[0])
            two = str(sub_args[1])

            # if the first argument starts with an ~ sign, we negate it, meaning
            # that we remove it. If it does not have one, we negate it as well
            # meaning that we add a ~ sign to it
            if one[0] == "~":
                one = one[1:]
            else:
                one = "~" + one

            # if the second argument starts with an ~ sign, we negate it, meaning
            # that we remove it. If it does not have one, we negate it as well
            # meaning that we add a ~ sign to it
            if two[0] == "~":
                two = two[1:]
            else:
                two = "~" + two

            # return the recursion call on the altered sub expression
            sub.args = (expr(one), expr(two))
            return deMorgansLaw(sub)

    # if the operator is just a letter, it means there is no other operator
    # present so we just return the letter
    if is_symbol(op) == True:
        return s

    # if the operator is an & or an | then return the recursive call of the
    # first argument plus the operator (& or |) plus the recursive call of the
    # second argument
    if op == "&" or op == "|":
        return expr(str(deMorgansLaw(args[0])) + op + str(deMorgansLaw(args[1])))



# ______________________________________________________________________________
# STEP3: use Distibutive Law to distribute and('&') over or('|')


""" Example:
>>> distibutiveLaw((A & B) | C)
((A | C) & (B | C))
"""

# TODO: apply distibutiveLaw so as to return an equivalent expression in CNF form
# Hint: you may use the associate() helper function to help you flatten the expression
def distibutiveLaw(s):
    # assign the operator and arguments
    op = s.op
    args = s.args

    # if the expression only contains &'s or only contains |'s, we just return
    # the expression as it is, as there is no dsitributing to do in such a case
    if "&" not in str(s) or "|" not in str(s):
        return s

    # if the operator is an &, we want to recurse on the arguments of the
    # expression. we call the recursive function on the first argument, add
    # that to the operator, and then add those to what is returned when calling
    # the recursive function on the second argument
    if op == "&":
        return expr(str(distibutiveLaw(args[0])) + op + str(distibutiveLaw(args[1])))

    # if the operator is |, we follow this path
    if op == "|":
        # two arguments
        one = args[0]
        two = args[1]

        # if there is an & in the first argument, we follow this path
        if "&" in str(one):
            # operator and arguments of the first argument
            sub_op = one.op
            sub_args = one.args

            # if the sub operator is an |, we recurse on the first argument and
            # add that to the operator and the second argument. We then recurse
            # on that entire altered expression
            if sub_op == "|":
                return distibutiveLaw(expr(str(distibutiveLaw(one)) + op + str(two)))

            # if the sub operator is an &, we distribute, so that (A&B) | C
            # becomes (A | C) & (B | C). We call the recursive distributive
            # function on each of the two arguments in the altered expression
            # above
            if sub_op == "&":
                return expr(str(distibutiveLaw(expr(str(sub_args[0]) + op + str(two)))) + sub_op + str(distibutiveLaw(expr(str(sub_args[1]) + op + str(two)))))

        # if there is an & in the second argument but not in the first  argument,
        # we follow this path
        if "&" in str(two):
            # operator and arguments of the second argument
            sub_op = two.op
            sub_args = two.args

            # if the sub operator is an |, we recurse on the first argument and
            # add that to the operator and the second argument. We then recurse
            # on that entire altered expression
            if sub_op == "|":
                return distibutiveLaw(expr(str(one) + op + str(distibutiveLaw(two))))

            # if the sub operator is an &, we distribute, so that C | (A&B)
            # becomes (C | A) & (C | B). We call the recursive distributive
            # function on each of the two arguments in the altered expression
            # above
            if sub_op == "&":
                return expr(str(distibutiveLaw(expr(str(one) + op + str(sub_args[0])))) + sub_op + str(distibutiveLaw(expr(str(one) + op + str(sub_args[1])))))



# ______________________________________________________________________________

# DO NOT CHANGE SAT_solver
# Check satisfiability of an arbitrary looking Boolean Expression.
# It returns a satisfying assignment(Non-deterministic, non exhaustive) when it succeeds.
# returns False if the formula is unsatisfiable
# Don't need to care about the heuristic part


""" Example:
>>> SAT_solver(A |'<=>'| B) == {A: True, B: True}
True
"""

""" unsatisfiable example:
>>> SAT_solver(A & ~A )
False
"""
def SAT_solver(s, heuristic=no_heuristic):
    return dpll(conjuncts(to_cnf_gadget(s)), prop_symbols(s), {}, heuristic)


# main function with test cases
if __name__ == "__main__":

# Initialization
    A, B, C, D, E, F = expr('A, B, C, D, E, F')
    P, Q, R = expr('P, Q, R')

# Shows alternative ways to write your expression
    assert SAT_solver(A | '<=>' | B) == {A: True, B: True}
    assert SAT_solver(expr('A <=> B')) == {A: True, B: True}   

# Some unsatisfiable examples
    assert SAT_solver(P & ~P) is False
    # The whole expression below is essentially just (A&~A)
    assert SAT_solver((A | B | C) & (A | B | ~C) & (A | ~B | C) & (A | ~B | ~C) & (
        ~A | B | C) & (~A | B | ~C) & (~A | ~B | C) & (~A | ~B | ~C)) is False

# This is the same example in the instructions.
    # Notice that SAT_solver's return value  is *Non-deterministic*, and *Non-exhaustive* when the expression is satisfiable,
    # meaning that it will only return *a* satisfying assignment when it succeeds.
    # If you run the same instruction multiple times, you may see different returns, but they should all be satisfying ones.
    result = SAT_solver((~(P | '==>' | Q)) | (R | '==>' | P))
    assert pl_true((~(P | '==>' | Q)) | (R | '==>' | P), result)

    assert pl_true((~(P | '==>' | Q)) | (R | '==>' | P), {P: True})
    assert pl_true((~(P | '==>' | Q)) | (R | '==>' | P), {Q: False, R: False})
    assert pl_true((~(P | '==>' | Q)) | (R | '==>' | P), {R: False})

# Some Boolean expressions has unique satisfying solutions
    assert SAT_solver(A & ~B & C & (A | ~D) & (~E | ~D) & (C | ~D) & (~A | ~F) & (E | ~F) & (~D | ~F) &
                      (B | ~C | D) & (A | ~E | F) & (~A | E | D)) == \
        {B: False, C: True, A: True, F: False, D: True, E: False}
    assert SAT_solver(A & B & ~C & D) == {C: False, A: True, D: True, B: True}
    assert SAT_solver((A | (B & C)) | '<=>' | ((A | B) & (A | C))) == {
        C: True, A: True} or {C: True, B: True}
    assert SAT_solver(A & ~B) == {A: True, B: False}

# The order in which the satisfying variable assignments get returned doen't matter.
    assert {A: True, B: False} == {B: False, A: True}
    print("No assertion errors found so far")
