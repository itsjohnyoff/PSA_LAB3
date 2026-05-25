from tweet_analyzer import clean_and_tokenize, get_popular_nouns_with_rating

data = clean_and_tokenize()
popular_nouns = get_popular_nouns_with_rating(data["nouns"], data["word_likes"], data["word_retweets"])

print("--- 10 Most Popular Nouns (By Rating Formula) ---")
for noun, score in popular_nouns[:10]:
    print(f"{noun} (Score: {score:.2f})")