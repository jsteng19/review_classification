import math
import sys
import time


def train(training, alpha):

    training_data = parse(training)
    p_count, n_count = 0, 0
    p_word_dict, n_word_dict = {}, {}
    p_pair_dict, n_pair_dict = {}, {}
    for review in training_data:
        pairs = []
        for i in range(len(review[0]) - 1):
            pairs.append(review[0][i] + " " + review[0][i + 1])

        words = set(review[0])
        if review[1] == 0:
            n_count += 1
            word_dict = n_word_dict
            pair_dict = n_pair_dict

        else:
            p_count += 1
            word_dict = p_word_dict
            pair_dict = p_pair_dict

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

    p_word_sum = sum(p_word_dict.values())
    n_word_sum = sum(n_word_dict.values())

    vocabulary = set().union(p_word_dict.keys(), n_word_dict.keys())
    p_word_dict.update([(word, 0) for word in vocabulary - set(p_word_dict.keys())])
    n_word_dict.update([(word, 0) for word in vocabulary - set(n_word_dict.keys())])

    p_pair_sum = sum(p_pair_dict.values())
    n_pair_sum = sum(n_pair_dict.values())

    pair_vocabulary = set().union(p_pair_dict.keys(), n_pair_dict.keys())
    p_pair_dict.update([(word, 0) for word in pair_vocabulary - set(p_pair_dict.keys())])
    n_pair_dict.update([(word, 0) for word in pair_vocabulary - set(n_pair_dict.keys())])






    # p_positive = {word: math.log((p_word_dict[word] + alpha) / (p_word_sum + alpha * len(vocabulary)))
    #                    for word in vocabulary}
    #
    # p_negative = {word: math.log((n_word_dict[word] + alpha) / (n_word_sum + alpha * len(vocabulary)))
    #                    for word in vocabulary}

    p_positive = {pair: math.log((p_pair_dict[pair] + alpha) / (p_pair_sum + alpha * len(pair_vocabulary)))
                  for pair in pair_vocabulary}

    p_negative = {pair: math.log((n_pair_dict[pair] + alpha) / (n_pair_sum + alpha * len(pair_vocabulary)))
                  for pair in pair_vocabulary}

    return p_positive, p_negative, vocabulary, pair_vocabulary


def test(testing, p_positive, p_negative, vocabulary, pair_vocabulary):

    testing_data = parse(testing)

    labels = ""

    linecount, correctcount = 0, 0
    for review in testing_data:
        positive, negative = 0, 0
        # for word in review[0]:
        #     if word in vocabulary:
        #         positive += p_positive[word]
        #         negative += p_negative[word]

        for i in range(len(review[0]) - 1):
            pair = review[0][i] + " " + review[0][i + 1]
            if pair in pair_vocabulary:
                positive += p_positive[pair]
                negative += p_negative[pair]

        if negative > positive:
            labels += "0\n"
            if review[1] == 0:
                correctcount += 1
            # else:
                # print("False negative: " + " ".join(review[0]))
        else:
            labels += "1\n"
            if review[1] == 1:
                correctcount += 1
            # else:
                # print("False positive: " + " ".join(review[0]))

        linecount += 1


    accuracy = correctcount / linecount
    labels = labels[:-1]
    return accuracy, labels


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
    t = time.perf_counter()
    p_positive, p_negative, vocabulary, pair_vocabulary = train(sys.argv[1], 1)
    training_time = time.perf_counter() - t

    t = time.perf_counter()
    testing_accuracy, testing_labels = test(sys.argv[2], p_positive, p_negative, vocabulary, pair_vocabulary)
    testing_time = time.perf_counter() - t

    print(testing_labels)
    print(str(round(training_time)) + " seconds (training)")
    print(str(round(testing_time)) + " seconds (testing)")

    training_accuracy, training_labels = test(sys.argv[1], p_positive, p_negative, vocabulary, pair_vocabulary)
    print(str(round(training_accuracy, 3)) + " (training)")
    print(str(round(testing_accuracy, 3)) + " (testing)")


main()
