import collections
from tweet_analyzer import clean_and_tokenize

data = clean_and_tokenize()
next_word_map = data["next_word_map"]

word = input("Enter a word to get next-word suggestions: ").lower()

# count how often each word follows the input word
following_words = next_word_map.get(word, [])

if not following_words:
    print(f"No suggestions found for '{word}'.")
else:
    counter = collections.Counter(following_words)
    print(f"\nNext-word suggestions for '{word}':")
    for next_word, count in counter.most_common(3):
        print(f"-> {next_word} ({count})")
