"""
Tingrui Zhang

Basic algorithms module

Algorithms for efficiently counting and sorting distinct 'entities',
or unique values, are widely used in data analysis.
"""

import math
from util import sort_count_pairs

# Task 1.1
def count_tokens(tokens):
    '''
    Counts each distinct token (entity) in a list of tokens.

    Inputs:
        tokens: list of tokens (must be immutable)

    Returns: dictionary that maps tokens to counts
    '''

    dict1 = {}

    for token in tokens:
        if token not in dict1.keys():
            dict1[token] = 1
        else:
            dict1[token] += 1

    return dict1


# Task 1.2
def find_top_k(tokens, k):
    '''
    Find the k most frequently occuring tokens.

    Inputs:
        tokens: list of tokens (must be immutable)
        k: a non-negative integer

    Returns: list of the top k tokens ordered by count.
    '''

    if k < 0:
        raise ValueError("In find_top_k, k must be a non-negative integer")
    
    lst = []
    lst_k = []
    dict1 = count_tokens(tokens)

    # Convert count data into a list of (token, count) tuples
    for key, value in dict1.items():
        token = (key,value)
        lst.append(token)

    # Sort the list via given function
    sorted_lst = sort_count_pairs(lst)
    
    # Extract the k tokens that occurred most frequently
    sorted_lst = sorted_lst[:k]
    for token1 in sorted_lst:
        lst_k.append(token1[0])

    return lst_k


# Task 1.3
def find_min_count(tokens, min_count):
    '''
    Find the tokens that occur *at least* min_count times.

    Inputs:
        tokens: a list of tokens  (must be immutable)
        min_count: a non-negative integer

    Returns: set of tokens
    '''

    if min_count < 0:
        raise ValueError("min_count must be a non-negative integer")
    
    dict1 = count_tokens(tokens)
    mincount_set = set()

    # In count dictionary, add token to set if count exceeds min_count
    for token, count in dict1.items():
        if count >= min_count:
            mincount_set.add(token)

    return mincount_set


# Task 1.4
def calculate_tf(doc):
    '''
    Calculates the augmented frequency of words in a document
     
    Input:
      doc: list of tokens

    Returns: dictionary of words and tf values
      '''
    
    dict1 = count_tokens(doc)
    tf_dict = {}
    
    # In case the doc is empty, return empty tf_dict
    try:
        max_number = max(dict1.values())
    except:
        return tf_dict
    
    # Calculate tf
    for token, count in dict1.items():
        tf_dict[token] = 0.5 + 0.5 * (count / max_number)

    return tf_dict


def calculate_idf(docs):
    '''
    Calculates the inverse document frequency of words in a 
    list of documents
     
    Input:
      docs: list of list of tokens

    Returns: dictionary of words and idf values
      '''
    D = len(docs) 
    idf_dict = {}

    # obtain unique tokens
    for doc in docs:
        for token in doc:
            if token not in idf_dict.keys():
                idf_dict[token] = 0
    
    # count number of documents that a token occurs in
    for word in idf_dict.keys():
        for doc in docs:
            if word in doc:
                idf_dict[word] += 1

    #calculate idf
    for token1, count in idf_dict.items():
        idf_dict[token1] = math.log(D / count)

    return idf_dict


def find_salient_one(doc, threshold, idf_dict):
    '''
    Compute the salient words for one document.  A word is salient if
    its tf-idf score is strictly above a given threshold.

    Inputs:
      doc: list of tokens
      threshold: float
      idf_dict: dictionary of tokens and their idf values

    Returns: a set of salient words
    '''
    salient = set()
    tf_dict = calculate_tf(doc)

    # Calculate tf-idf values for tokens in each doc
    # and add it to set if tf-idf exceeds threshold
    for token, tf in tf_dict.items():
        tfidf = tf * idf_dict[token]
        if tfidf > threshold:
            salient.add(token)

    return salient


def find_salient(docs, threshold):
    '''
    Compute the salient words for each document.  A word is salient if
    its tf-idf score is strictly above a given threshold.

    Inputs:
      docs: list of list of tokens
      threshold: float

    Returns: list of sets of salient words
    '''
    idf_dict = calculate_idf(docs)
    salient = []

    for doc in docs:
        salient.append(find_salient_one(doc, threshold, idf_dict))
    
    return salient
