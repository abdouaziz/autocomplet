import random
import math
import numpy as np
import pandas as pd
import nltk
nltk.data.path.append('.')


with open("data.txt", encoding="utf-8") as f:
    data = f.read()


def split_data(data):
    sentences = data.split('\n')
    sentences = [s.strip() for s in sentences]
    sentences = [s for s in sentences if len(s) > 2]

    return sentences


def tokenize_sentence(sentences):

    tokenized_sentences = []

    for sentence in sentences:
        sentence = sentence.lower()
        tokenized = nltk.word_tokenize(sentence)
        tokenized_sentences.append(tokenized)

    return tokenized_sentences


def get_tokenized_data(data):
    sentences = split_data(data)
    tokenized_sentences = tokenize_sentence(sentences)

    return tokenized_sentences


tokenized_data = get_tokenized_data(data)
random.seed(87)
random.shuffle(tokenized_data)

train_size = int(len(tokenized_data) * 0.8)
train_data = tokenized_data[0:train_size]
test_data = tokenized_data[train_size:]


def count_words(tokenized_sentences):
    word_counts = {}

    for sentence in tokenized_sentences:
        for token in sentence:
            if token not in word_counts.keys():
                word_counts[token] = 1
            else:
                word_counts[token] += 1

    return word_counts


def get_words_with_nplus_frequency(tokenized_sentences, count_threshold):

    closed_vocab = []
    word_counts = count_words(tokenized_sentences)

    for word, cnt in word_counts.items():
        if cnt >= count_threshold:
            closed_vocab.append(word)

    return closed_vocab


def replace_oov_words_by_unk(tokenized_sentences, vocabulary, unknown_token="<unk>"):

    vocabulary = set(vocabulary)

    replaced_tokenized_sentences = []

    for sentence in tokenized_sentences:

        replaced_sentence = []

        for token in sentence:

            if token in vocabulary:

                replaced_sentence.append(token)
            else:

                replaced_sentence.append(unknown_token)

        replaced_tokenized_sentences.append(replaced_sentence)

    return replaced_tokenized_sentences


def preprocess_data(train_data, test_data, count_threshold=2):

    vocabulary = get_words_with_nplus_frequency(train_data, count_threshold)

    train_data_replaced = replace_oov_words_by_unk(train_data, vocabulary)

    test_data_replaced = replace_oov_words_by_unk(test_data, vocabulary)

    return train_data_replaced, test_data_replaced, vocabulary


def count_n_grams(data, n, start_token='<s>', end_token='<e>'):

    n_grams = {}

    for sentence in data:

        sentence = [start_token] * n + sentence + [end_token]

        sentence = tuple(sentence)

        m = len(sentence) if n == 1 else len(sentence)-1
        for i in range(m):

            n_gram = sentence[i:i+n]

            if n_gram in n_grams.keys():

                n_grams[n_gram] += 1
            else:

                n_grams[n_gram] = 1

    return n_grams


def estimate_probability(word, previous_n_gram,
                         n_gram_counts, n_plus1_gram_counts, vocabulary_size, k=1.0):

    previous_n_gram = tuple(previous_n_gram)

    previous_n_gram_count = n_gram_counts[previous_n_gram] if previous_n_gram in n_gram_counts else 0

    denominator = previous_n_gram_count + k * vocabulary_size

    n_plus1_gram = previous_n_gram + (word,)

    n_plus1_gram_count = n_plus1_gram_counts[n_plus1_gram] if n_plus1_gram in n_plus1_gram_counts else 0

    numerator = n_plus1_gram_count + k

    probability = numerator / denominator

    return probability


def estimate_probabilities(previous_n_gram, n_gram_counts, n_plus1_gram_counts, vocabulary, k=1.0):

    previous_n_gram = tuple(previous_n_gram)

    vocabulary = vocabulary + ["<e>", "<unk>"]
    vocabulary_size = len(vocabulary)

    probabilities = {}
    for word in vocabulary:
        probability = estimate_probability(word, previous_n_gram,
                                           n_gram_counts, n_plus1_gram_counts,
                                           vocabulary_size, k=k)
        probabilities[word] = probability

    return probabilities


def make_count_matrix(n_plus1_gram_counts, vocabulary):

    vocabulary = vocabulary + ["<e>", "<unk>"]

    n_grams = []
    for n_plus1_gram in n_plus1_gram_counts.keys():
        n_gram = n_plus1_gram[0:-1]
        n_grams.append(n_gram)
    n_grams = list(set(n_grams))

    row_index = {n_gram: i for i, n_gram in enumerate(n_grams)}

    col_index = {word: j for j, word in enumerate(vocabulary)}

    nrow = len(n_grams)
    ncol = len(vocabulary)
    count_matrix = np.zeros((nrow, ncol))
    for n_plus1_gram, count in n_plus1_gram_counts.items():
        n_gram = n_plus1_gram[0:-1]
        word = n_plus1_gram[-1]
        if word not in vocabulary:
            continue
        i = row_index[n_gram]
        j = col_index[word]
        count_matrix[i, j] = count

    count_matrix = pd.DataFrame(
        count_matrix, index=n_grams, columns=vocabulary)
    return count_matrix


def make_probability_matrix(n_plus1_gram_counts, vocabulary, k):
    count_matrix = make_count_matrix(n_plus1_gram_counts, unique_words)
    count_matrix += k
    prob_matrix = count_matrix.div(count_matrix.sum(axis=1), axis=0)
    return prob_matrix


def calculate_perplexity(sentence, n_gram_counts, n_plus1_gram_counts, vocabulary_size, k=1.0):

    n = len(list(n_gram_counts.keys())[0])

    sentence = ["<s>"] * n + sentence + ["<e>"]

    sentence = tuple(sentence)

    N = len(sentence)

    product_pi = 1.0

    for t in range(n, N):

        n_gram = sentence[t-n:t]

        word = sentence[t]

        probability = estimate_probability(
            word, n_gram, n_gram_counts, n_plus1_gram_counts, len(unique_words), k=1)

        product_pi *= 1 / probability

    perplexity = product_pi**(1/float(N))

    return perplexity


def suggest_a_word(previous_tokens, n_gram_counts, n_plus1_gram_counts, vocabulary, k=1.0, start_with=None):

    n = len(list(n_gram_counts.keys())[0])

    previous_n_gram = previous_tokens[-n:]

    probabilities = estimate_probabilities(previous_n_gram,
                                           n_gram_counts, n_plus1_gram_counts,
                                           vocabulary, k=k)

    suggestion = None

    max_prob = 0

    for word, prob in probabilities.items():

        if start_with != None:

            if not word.startswith(start_with):

                continue

        if prob > max_prob:

            suggestion = word

            max_prob = prob

    return suggestion, max_prob


def get_suggestions(previous_tokens, n_gram_counts_list, vocabulary, k=1.0, start_with=None):
    model_counts = len(n_gram_counts_list)
    suggestions = []
    for i in range(model_counts-1):
        n_gram_counts = n_gram_counts_list[i]
        n_plus1_gram_counts = n_gram_counts_list[i+1]

        suggestion = suggest_a_word(previous_tokens, n_gram_counts,
                                    n_plus1_gram_counts, vocabulary,
                                    k=k, start_with=start_with)
        suggestions.append(suggestion)
    return suggestions


unique_words = [set(token) for token in train_data]


minimum_freq = 2
train_data_processed, test_data_processed, vocabulary = preprocess_data(train_data, test_data,minimum_freq)
                                                                       
                                                                        

 


 