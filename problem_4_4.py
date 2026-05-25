import matplotlib.pyplot as plt
from tweet_analyzer import clean_and_tokenize

data = clean_and_tokenize()
search_word = input("Enter a word for the frequency chart: ").lower()

monthly_data = data["word_monthly_freq"].get(search_word, {})

if not monthly_data:
    print(f"Word '{search_word}' not found in the dataset.")
else:
    # sort months chronologically
    sorted_months = sorted(monthly_data.keys())
    frequencies = [monthly_data[m] for m in sorted_months]

    plt.figure(figsize=(10, 5))
    plt.bar(sorted_months, frequencies, color='#2b5c8f', edgecolor='#1a3a60')
    plt.xlabel('Month')
    plt.ylabel('Frequency')
    plt.title(f"Monthly Frequency for '{search_word}'")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()