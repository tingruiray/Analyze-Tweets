Election Tweets Analysis
Tingrui Zhang

------------------------------------------------------------------------------------
In this code we will:

Analyze tweets sent from the official Twitter accounts of four parties: 
the Conservative and Unionist Party (@Conservatives), the Labour Party (@UKLabour),
the Liberal Democrats (@LibDems) and the Scottish National Party (@theSNP) 
during purdah (2017 General Election campaign). We’ll ask questions such as:

What was @Conservatives’s favorite hashtag during purdah? 
[#bbcqt]

Who was mentioned at least 50 times by @UKLabour? 
[@jeremycorbyn]

What words occurred most often in @theSNP’s tweets? 
[snp, scotland, our, have, more]

What two-word phrases occurred most often in @LibDems’s tweets? 
[stand up, stop tories, will stand, theresa may, lib dems]



------------------------------------------------------------------------------------
- basic_algorithms.py: Includes helper functions.

count_tokens(tokens) – Counts distinct tokens.
find_top_k(tokens, k) – Finds the top k most frequent tokens (with alphabetical tie-breaking).
find_min_count(tokens, min_count) – Returns all tokens that appear at least min_count times.
find_salient(docs, threshold) – Computes the most salient tokens in each document 
  using TF–IDF weighting.
These algorithms are reusable building blocks for later tweet and text analyses.


- analyze.py: Core functions to analyze tweets.

find_top_k_entities(tweets, entity_desc, k) – Finds the k most frequent entities 
  (e.g., hashtags).
find_min_count_entities(tweets, entity_desc, min_count) – 
  Finds entities appearing at least min_count times.
find_top_k_ngrams(tweets, n, case_sensitive, k) – 
  Finds top k most frequent n-grams.
find_min_count_ngrams(tweets, n, case_sensitive, min_count) – 
  Finds n-grams occurring at least min_count times.
find_salient_ngrams(tweets, n, case_sensitive, threshold) – 
  Identifies salient n-grams using TF–IDF (stop words not removed).

Example outputs:

Most used SNP hashtags → ['votesnp', 'ge17', 'snpbecause']
Frequent LibDem mentions → {'LibDems', 'LibDemPress', 'timfarron'}
SNP’s top bigrams → [('nicola', 'sturgeon'), ('read', 'more'), ('stand', 'up')]
LibDem frequent phrases → {('stop', 'Tories'), ('will', 'stand'), ('Theresa', 'May')}


- util.py: Code containing helper functions. You will only use the function
  sort_count_pairs directly.

- get_files.sh: A script for downloading the data. See the programming 
  assignment writeup for instructions on how to run it. Running it will add two
  new directories: data/ and tests/

- load_tweets.py: Code for loading the tweets in the data set in Python (after
  the data has been downloaded).

- test_basic_algorithms.py, test_analyze.py: The automated tests. See the
  programming assignment writeup for instructions on how to run them.

- test_helpers.py: Helper functions for the automated tests. You will not need
  to interact with this file directly.

- pytest.ini, .pylintrc, .gitignore: Configuration files that you can safely ignore.

- README.txt: This file.


------------------------------------------------------------------------------------
The data for this code should be downloaded from the link:

https://www.classes.cs.uchicago.edu/archive/2020/fall/30121-1/pa-data/pa3.tgz 

(1) open the link in your web browser, and you will see a pop-up screen showing that pa3.tgz 
has been downloaded to the default location on your computer (that's typically "Downloads" folder) 

(2) unzip pa3.tgz and you will see two folders data and tests, drag the two folders to your 
PA3 repository.