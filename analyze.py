"""
Tingrui Zhang

Analyze module

Functions to analyze tweets. 
"""

import unicodedata
import sys

from basic_algorithms import find_top_k, find_min_count, find_salient

def keep_chr(ch):
    '''
    Find all characters that are classifed as punctuation in Unicode
    (except #, @, &) and combine them into a single string.
    '''
    return unicodedata.category(ch).startswith('P') and \
        (ch not in ("#", "@", "&"))

PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                        if keep_chr(chr(i))])

# When processing tweets, ignore these words
STOP_WORDS = ["a", "an", "the", "this", "that", "of", "for", "or",
              "and", "on", "to", "be", "if", "we", "you", "in", "is",
              "at", "it", "rt", "mt", "with"]

# When processing tweets, words w/ a prefix that appears in this list
# should be ignored.
STOP_PREFIXES = ("@", "#", "http", "&amp")


############## Part 2 ##############

# Task 2.1
def list_entities(tweets, entity_desc):
    '''
    Create a list of occurances of entities of interest

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple such as ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc.

    Returns: list of entity occurances
    '''
    entity_lst = []
    entity_type, subkey, case_sensitive = entity_desc

    # Append entity occurance to list, if any
    for tweet in tweets:
        try:
            for entity in tweet['entities'][entity_type]:
                value = entity.get(subkey)
                if value:
                    if not case_sensitive:
                        value = value.lower()
                    entity_lst.append(value)
        except:
            continue

    return entity_lst


def find_top_k_entities(tweets, entity_desc, k):
    '''
    Find the k most frequently occuring entitites.

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple such as ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc.
        k: integer

    Returns: list of entities
    '''
    entity_lst = list_entities(tweets, entity_desc)

    # count entity occurance and find top k
    lst = find_top_k(entity_lst, k)

    return lst



# Task 2.2
def find_min_count_entities(tweets, entity_desc, min_count):
    '''
    Find the entitites that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple such as ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc.
        min_count: integer

    Returns: set of entities
    '''

    entity_lst = list_entities(tweets, entity_desc)

    mincount_set = find_min_count(entity_lst, min_count)
    
    return mincount_set



############## Part 3 ##############

# Pre-processing step and representing n-grams

def list_clean_words(abridged_text):
    '''
    Turn the abridged text of a tweet into a list of words, 
    remove leading and trailing punctuations,
    eliminate a word if stripping the punctuation from it yields 
    the empty string, and remove URLs, hashtags, and mentions

    Inputs:
        abridged_text: abridged version of the texts

    Returns: list of words
    '''
    lst = abridged_text.split()
    clean_lst = []

    for word in lst:
        # Ignore empty strings and URLs, hashtags, and mentions
        if not word or \
            any(word.startswith(prefix) for prefix in STOP_PREFIXES):
            continue
            
        # Remove leading punctuation (remove multiple if needed)
        while word and word[0] in PUNCTUATION:
            word = word[1:]
        
        # Remove trailing punctuation (remove multiple if needed)
        while word and word[-1] in PUNCTUATION:
            word = word[:-1]
        
        # Append non-empty and cleaned text
        if word and \
            not any(word.startswith(prefix) for prefix in STOP_PREFIXES):
            clean_lst.append(word)

    return clean_lst


def convert_case(lst):
    '''
    Convert the word to lower case.

    Inputs:
        lst: a list of words

    Returns: list of words with case converted
    '''
    lower_lst = []

    for word in lst:
        lower_lst.append(word.lower())

    return lower_lst


def eliminate_stop_words(lst):
    '''
    Eliminate all stop words for a word list.
    
    Inputs:
        lst: a list of words

    Returns: list of words with stop words removed
    ''' 
    removed_lst = []

    for word in lst:
        if word not in STOP_WORDS:
            removed_lst.append(word)

    return removed_lst

def find_ngram(lst, n):
    '''
    Converts a list of words into ngram.
    Inputs:
        lst: a list of words
        n: integer

    Returns: list of n-grams
    '''
    ngram = []

    for i in range(len(lst)- n + 1):
        ngram.append(lst[i:i+n])

    return ngram


# Task 3.1
def find_top_k_ngrams(tweets, n, case_sensitive, k):
    '''
    Find k most frequently occurring n-grams.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        k: integer

    Returns: list of n-grams
    '''
    ngram = []
    
    # Abstract abridged text, clean them, and create ngram
    for tweet in tweets:
        abridged_text = tweet["abridged_text"]
        if case_sensitive:
            clean_lst = eliminate_stop_words\
                (list_clean_words(abridged_text))
        else:
            clean_lst = eliminate_stop_words\
                (convert_case(list_clean_words(abridged_text)))
        
        tweet_ngrams = find_ngram(clean_lst, n)

        # Convert ngram into tuples to fit into helper function
        tweet_ngrams = [tuple(gram) for gram in tweet_ngrams]
        ngram.extend(tweet_ngrams)
    
    lst = find_top_k(ngram, k)

    return lst


# Task 3.2
def find_min_count_ngrams(tweets, n, case_sensitive, min_count):
    '''
    Find n-grams that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        min_count: integer

    Returns: set of n-grams
    '''

    ngram = []
    
    # Abstract abridged text, clean them, and create ngram
    for tweet in tweets:
        abridged_text = tweet["abridged_text"]
        if case_sensitive:
            clean_lst = eliminate_stop_words(list_clean_words(abridged_text))
        else:
            clean_lst = eliminate_stop_words(convert_case(list_clean_words(abridged_text)))
        
        tweet_ngrams = find_ngram(clean_lst, n)

        # Convert ngram into tuples to fit into helper function
        tweet_ngrams = [tuple(gram) for gram in tweet_ngrams]
        ngram.extend(tweet_ngrams)

    mincount_set = find_min_count(ngram, min_count)

    return mincount_set


# Task 3.3
def find_salient_ngrams(tweets, n, case_sensitive, threshold):
    '''
    Find the salient n-grams for each tweet.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        threshold: float

    Returns: list of sets of strings
    '''
    ngram = []
    
    # Abstract abridged text, clean them, and create ngram
    for tweet in tweets:
        abridged_text = tweet["abridged_text"]
        if case_sensitive:
            clean_lst = list_clean_words(abridged_text)
        else:
            clean_lst = convert_case(list_clean_words(abridged_text))
        
        tweet_ngrams = find_ngram(clean_lst, n)
        tweet_ngrams = [tuple(gram) for gram in tweet_ngrams]

        ngram.append(tweet_ngrams)

        lst = find_salient(ngram, threshold)
    
    return lst
