import json
import collections
import re
import nltk

# download NLTK data if missing
try:
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    nltk.download('punkt_tab', quiet=True)
    nltk.download('averaged_perceptron_tagger_eng', quiet=True)

def load_tweets(filepath="tweets.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_and_tokenize():
    tweets = load_tweets()

    all_words = []
    nouns = []
    proper_nouns = []

    # accumulate likes/retweets per word for popularity scoring
    word_likes = collections.defaultdict(int)
    word_retweets = collections.defaultdict(int)

    # monthly frequency: word -> "YYYY-MM" -> count
    word_monthly_freq = collections.defaultdict(lambda: collections.defaultdict(int))

    # bigram map for next-word prediction
    next_word_map = collections.defaultdict(list)

    for tweet in tweets:
        text = tweet.get("text", "")
        likes = tweet.get("likes", 0)
        retweets = tweet.get("retweets", 0)
        date_str = tweet.get("created_at", "")
        month = date_str[:7]

        # strip URLs and @mentions before tokenizing
        text = re.sub(r'https?://\S+', '', text)
        text = re.sub(r'@\w+', '', text)

        tokens = nltk.word_tokenize(text)
        tagged_tokens = nltk.pos_tag(tokens)

        cleaned_tweet_words = []

        for word, tag in tagged_tokens:
            clean_word = re.sub(r'[^\w]', '', word)
            if not clean_word:
                continue

            clean_word_lower = clean_word.lower()
            cleaned_tweet_words.append(clean_word_lower)
            all_words.append(clean_word_lower)

            word_likes[clean_word_lower] += likes
            word_retweets[clean_word_lower] += retweets
            word_monthly_freq[clean_word_lower][month] += 1

            # NN/NNS = common nouns, NNP/NNPS = proper nouns
            if tag in ("NN", "NNS"):
                nouns.append(clean_word_lower)
            elif tag in ("NNP", "NNPS"):
                proper_nouns.append(clean_word)

        # build bigrams for next-word suggestion
        for i in range(len(cleaned_tweet_words) - 1):
            next_word_map[cleaned_tweet_words[i]].append(cleaned_tweet_words[i + 1])

    return {
        "all_words": all_words,
        "nouns": nouns,
        "proper_nouns": proper_nouns,
        "word_likes": word_likes,
        "word_retweets": word_retweets,
        "word_monthly_freq": word_monthly_freq,
        "next_word_map": next_word_map
    }

def get_popular_nouns_with_rating(nouns, word_likes, word_retweets):
    noun_counts = collections.Counter(nouns)
    unique_nouns = list(noun_counts.keys())

    if not unique_nouns:
        return []

    # max-normalization baseline
    max_likes = max(word_likes[w] for w in unique_nouns) or 1
    max_retweets = max(word_retweets[w] for w in unique_nouns) or 1

    rated_nouns = []
    for noun in unique_nouns:
        freq = noun_counts[noun]
        norm_likes = word_likes[noun] / max_likes
        norm_retweet = word_retweets[noun] / max_retweets

        # popularity formula from assignment
        score = freq * (1.4 + norm_retweet) * (1.2 + norm_likes)
        rated_nouns.append((noun, score))

    rated_nouns.sort(key=lambda x: x[1], reverse=True)
    return rated_nouns
