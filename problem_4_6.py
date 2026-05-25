import collections
from tweet_analyzer import clean_and_tokenize

data = clean_and_tokenize()
global_counts = collections.Counter(data["all_words"])

prefix = input("Start typing a word (prefix): ").lower()

# find words matching the prefix, rank by frequency
suggestions = [word for word in global_counts if word.startswith(prefix)]
suggestions.sort(key=lambda w: global_counts[w], reverse=True)

print(f"\nSuggestions for '{prefix}':")
for word in suggestions[:3]:
    print(f"-> {word} ({global_counts[word]})")