"""
grammar.py module by Martin Prout
Supports the parsing of both stochastic and non-stochastic rules
axiom/rules are evaluated by the produce function, which uses the __weightedRule function
to return any stochastic rule according to the input dict, the repeat function is used to repeatedly
iterate the rules in a recursive fashion.
Example Rules:

Non-Stochastic = { "A": "A+F", "G": "GG", "X" :"G-G"}

Stochastic = {"A" : {"BCD": 5, "C+C+C":10, "ACA": 40}, "B" : {"DE-F": 5, "CCC":10, "A[C]A": 40}}

The Stochastic rule may contain non stochastic elements, in the above example there are two stochastic, elements,
with keys "A" and "B". The stochastic rule is detected by checking the 'value' type is dict. The dict needs to of the
form "string substitution" as key with the weighting as value.  A test function is included for the test conscious or
skeptic.
"""


import random

def __weightedRule(rules):
    """
    A private method used to choose a substitution rule from a dict of rules, according to its
    weighted probality. 'rules' is expected to be a dict where the substition string is the 'key' 
    and the 'value' is the rule weight
    """
    rand = random.random()
    prob = 0
    tot = sum(rules.values())     # sum probabilities
    for rule in rules.keys():     # iterate over rule choices
        prob += rules.get(rule)   # add assigned probalities
        if ((rand * tot) < prob): # compare running total with scaled random value
            return(rule)

def produce(axiom, rules):
    """
    The single rule substitution utility, that uses type to check for dict or str
    as key value, else declares 'Unrecognized grammar'. Does not throw exception!!!
    """
    str_buf = [] # list is much more efficient than premature string concatenation

    for i in axiom:
        temp = rules.get(i, i)
        if (type(temp) is dict):
            str_buf.append(__weightedRule(temp))
        elif (type(temp) is str):
            str_buf.append(temp)
        else:
            error = "Unknown rule type %s\n" % type(temp)
            print(error)
    return ''.join(str_buf) # join str_buf list as a single string
    
 
def repeat(rpx, axiom, rules):
    """
    Repeat rule substitution in a recursive fashion rpx times
    """ 
    production = axiom
    for i in range(0, rpx):
        production = produce(production, rules)
    return production
    
def __testWeighting(rules, key, total):     
    """
    Private test function see module header for examples of rules format
    Takes a dict containing a stochastic rule with 'key' as key.
    Tests the weighted rule function a 'total' number of times.
    Frequency result is printed.
    """
    wordList = [] # create a big test list of replacement rules
    for z in range(0, total):    
        wordList.append(__weightedRule(rules.get(key)))
        
    # calculate each word frequency in generated list (NB: does not test the
    # randomness of order though)
    freqD2 = {}
    for word2 in wordList:
        freqD2[word2] = freqD2.get(word2, 0) + 1
    keyList = freqD2.keys()
    keyList.sort()
    
    print "Frequency of each substitution string in the word list (sorted):"
    for key2 in keyList:
        print "%-10s %d" % (key2, freqD2[key2])
        
def toRuleString(axiom, rules):
    """
    Creates a string representing the pythonic rules in a more conventional
    manner
    """
    output = "Axiom:\t%s\n" % axiom 
    keys = rules.keys()
    for key in keys:
        temp = rules.get(key)
        type_temp =  type(temp)
        if (type_temp is dict):
            keys2 = temp.keys()
            for key2 in keys2:
                output += "Rule:\t%s => %s\t%d\n" % (key, key2, temp.get(key2))
        elif (type_temp is str):
            output += "Rule:\t%s => %s\n" % (key, temp)
        else:
            output += "Key:\t%s => %s an unknown rule type\n" % (key, type_temp)
    return output        
        

   
