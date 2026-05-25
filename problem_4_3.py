import collections
from tweet_analyzer import clean_and_tokenize

data = clean_and_tokenize()
counter = collections.Counter(data["proper_nouns"])

print("--- 10 Most Frequent Proper Nouns ---")
for word, freq in counter.most_common(10):
    print(f"{word} {freq}")