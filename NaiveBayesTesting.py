import math
import sys
import time


def train(training, smoothing_factors):

    training_data = parse(training)
    p_count, n_count = 0, 0

    p_word_dict, n_word_dict = {}, {}
    p_pair_dict, n_pair_dict = {}, {}
    p_triple_dict, n_triple_dict = {}, {}

    for review in training_data:
        words = set(review[0])

        pairs = []
        triples = []
        for i in range(len(review[0]) - 1):
            pairs.append(review[0][i] + " " + review[0][i + 1])

        for i in range(len(review[0]) - 2):
            triples.append(review[0][i] + " " + review[0][i + 1] + " " + review[0][i + 2])

        if review[1] == 0:
            n_count += 1
            word_dict = n_word_dict
            pair_dict = n_pair_dict
            triple_dict = n_triple_dict

        else:
            p_count += 1
            word_dict = p_word_dict
            pair_dict = p_pair_dict
            triple_dict = p_triple_dict

        for word in words:
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1

        for pair in pairs:
            if pair in pair_dict:
                pair_dict[pair] += 1
            else:
                pair_dict[pair] = 1

        for triple in triples:
            if triple in triple_dict:
                triple_dict[triple] += 1
            else:
                triple_dict[triple] = 1

    p_word_sum = sum(p_word_dict.values())
    n_word_sum = sum(n_word_dict.values())
    vocabulary = set().union(p_word_dict.keys(), n_word_dict.keys())
    p_word_dict.update([(word, 0) for word in vocabulary - set(p_word_dict.keys())])
    n_word_dict.update([(word, 0) for word in vocabulary - set(n_word_dict.keys())])


    p_pair_sum = sum(p_pair_dict.values())
    n_pair_sum = sum(n_pair_dict.values())
    pair_vocabulary = set().union(p_pair_dict.keys(), n_pair_dict.keys())
    p_pair_dict.update([(pair, 0) for pair in pair_vocabulary - set(p_pair_dict.keys())])
    n_pair_dict.update([(pair, 0) for pair in pair_vocabulary - set(n_pair_dict.keys())])

    p_triple_sum = sum(p_triple_dict.values())
    n_triple_sum = sum(n_triple_dict.values())
    triple_vocabulary = set().union(p_triple_dict.keys(), n_triple_dict.keys())
    p_triple_dict.update([(triple, 0) for triple in triple_vocabulary - set(p_triple_dict.keys())])
    n_triple_dict.update([(triple, 0) for triple in triple_vocabulary - set(n_triple_dict.keys())])


    p_positive = {word: math.log((p_word_dict[word] + smoothing_factors[0]) / (p_word_sum + smoothing_factors[0] * len(vocabulary)))
                       for word in vocabulary}

    p_negative = {word: math.log((n_word_dict[word] + smoothing_factors[0]) / (n_word_sum + smoothing_factors[0] * len(vocabulary)))
                       for word in vocabulary}

    word_probabilities = (p_negative, p_positive)

    p_positive = {pair: math.log((p_pair_dict[pair] + smoothing_factors[1]) / (p_pair_sum + smoothing_factors[1] * len(pair_vocabulary)))
                  for pair in pair_vocabulary}

    p_negative = {pair: math.log((n_pair_dict[pair] + smoothing_factors[1]) / (n_pair_sum + smoothing_factors[1] * len(pair_vocabulary)))
                  for pair in pair_vocabulary}

    pair_probabilities = (p_negative, p_positive)

    p_positive = {triple: math.log((p_triple_dict[triple] + smoothing_factors[2]) / (p_triple_sum + smoothing_factors[2] * len(triple_vocabulary)))
                  for triple in triple_vocabulary}

    p_negative = {triple: math.log((n_triple_dict[triple] + smoothing_factors[2]) / (n_triple_sum + smoothing_factors[2] * len(triple_vocabulary)))
                  for triple in triple_vocabulary}

    triple_probabilities = (p_negative, p_positive)


    probabilities = (word_probabilities, pair_probabilities, triple_probabilities)

    vocabularies = (vocabulary, pair_vocabulary, triple_vocabulary)

    return probabilities, vocabularies


def test(testing, probabilities, vocabularies, weights):

    testing_data = parse(testing)

    linecount, correctcount = 0, 0
    for review in testing_data:
        word_probability_pos, word_probability_neg = 0, 0
        for word in review[0]:
            if word in vocabularies[0]:
                word_probability_pos += probabilities[0][1][word]
                word_probability_neg += probabilities[0][0][word]

        pair_probability_pos, pair_probability_neg = 0, 0
        for i in range(len(review[0]) - 1):
            pair = review[0][i] + " " + review[0][i + 1]
            if pair in vocabularies[1]:
                pair_probability_pos += probabilities[1][1][pair]
                pair_probability_neg += probabilities[1][0][pair]

        triple_probability_pos, triple_probability_neg = 0, 0
        for i in range(len(review[0]) - 2):
            triple = review[0][i] + " " + review[0][i + 1] + " " + review[0][i + 2]
            if triple in vocabularies[2]:
                triple_probability_pos += probabilities[2][1][triple]
                triple_probability_neg += probabilities[2][0][triple]

        probability_pos = weights[0] * word_probability_pos + weights[1] * pair_probability_pos + weights[2] * triple_probability_pos
        probability_neg = weights[0] * word_probability_neg + weights[1] * pair_probability_neg + weights[2] * triple_probability_neg


        if probability_neg > probability_pos:

            if review[1] == 0:
                correctcount += 1
            # else:
                # print("False negative: " + " ".join(review[0]))
        else:
            if review[1] == 1:
                correctcount += 1
            # else:
                # print("False positive: " + " ".join(review[0]))

        linecount += 1

    accuracy = correctcount / linecount
    return accuracy


def parse(filename):

    parsed = []
    file = open(filename)
    for line in file:
        text, classification = line.rsplit(",")
        classification = 0 if classification == "0\n" else 1
        words = text.split()
        parsed.append((words, classification))

    return parsed


def main():
    smoothing_factors = [2, 0.6, .5]

    # t = time.perf_counter()
    # probabilities, vocabularies = train(sys.argv[1], smoothing_factors)
    # training_time = time.perf_counter() - t
    #
    # t = time.perf_counter()
    # testing_accuracy = test(sys.argv[2], probabilities, vocabularies)
    # testing_time = time.perf_counter() - t
    #
    # print(str(round(training_time)) + " seconds (training)")
    # print(str(round(testing_time)) + " seconds (testing)")

    # training_accuracy = test(sys.argv[1], p_positive, p_negative, vocabulary, pair_vocabulary)
    # # print(str(round(training_accuracy, 3)) + " (training)")
    # print(str(round(testing_accuracy, 3)) + " (testing)")

    # probabilities, vocabularies = train(sys.argv[1], smoothing_factors)
    # testing_accuracy = test(sys.argv[2], probabilities, vocabularies, [0, 0, 1])
    # print(str(round(testing_accuracy, 5)) + " (testing)")

    for weight in range(1, 10):
        probabilities, vocabularies = train(sys.argv[1], smoothing_factors)
        testing_accuracy = test(sys.argv[2], probabilities, vocabularies, [3, 10, weight])
        print("w = " + str(weight))
        print(str(round(testing_accuracy, 5)) + " (testing)")

    # for alpha in range(1, 10):
    #     probabilities, vocabularies = train(sys.argv[1], [1, 1, alpha / 10])
    #     testing_accuracy = test(sys.argv[2], probabilities, vocabularies, [0, 0, 1])
    #     print("a = " + str(alpha))
    #     print(str(round(testing_accuracy, 5)) + " (testing)")


main()
