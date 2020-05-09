import math
import sys
import time


def train(training, alpha):

    file = open(training)
    p_count, n_count = 0, 0
    p_dict, n_dict = {}, {}
    for line in file:
        text, classification = line.rsplit(",")
        words = set(text.split())
        if classification == "0\n":
            n_count += 1
            d = n_dict
        else:
            p_count += 1
            d = p_dict

        for word in words:
            if word in d:
                d[word] += 1
            else:
                d[word] = 1

    p_word_sum = sum(p_dict.values())
    n_word_sum = sum(n_dict.values())

    vocabulary = set().union(p_dict.keys(), n_dict.keys())
    n_dict.update([(word, 0) for word in vocabulary - set(n_dict.keys())])
    p_dict.update([(word, 0) for word in vocabulary - set(p_dict.keys())])


    p_positive = {word: math.log((p_dict[word] + alpha) / (p_word_sum + alpha * len(vocabulary)))
                       for word in vocabulary}

    p_negative = {word: math.log((n_dict[word] + alpha) / (n_word_sum + alpha * len(vocabulary)))
                       for word in vocabulary}

    return p_positive, p_negative, vocabulary


def test(testing, p_positive, p_negative, vocabulary):
    file = open(testing)

    labels = ""
    linecount, correctcount = 0, 0
    for line in file:
        text, classification = line.rsplit(",")
        words = text.split()
        positive, negative = 0, 0
        for word in words:
            if word in vocabulary:
                positive += p_positive[word]
                negative += p_negative[word]

        if negative > positive:
            labels += "0\n"
            if classification == "0\n":
                correctcount += 1
        else:
            labels += "1\n"
            if classification == "1\n":
                correctcount += 1

        linecount += 1

    labels = labels[:-1]
    accuracy = correctcount / linecount
    return labels, accuracy



def main():
    t = time.perf_counter()
    p_positive, p_negative, vocabulary = train(sys.argv[1], 2.1)
    training_time = time.perf_counter() - t

    t = time.perf_counter()
    testing_labels, testing_accuracy = test(sys.argv[2], p_positive, p_negative, vocabulary)
    testing_time = time.perf_counter() - t

    print(testing_labels)
    print(str(round(training_time)) + " seconds (training)")
    print(str(round(testing_time)) + " seconds (testing)")

    training_labels, training_accuracy = test(sys.argv[1], p_positive, p_negative, vocabulary)
    print(str(round(training_accuracy, 3)) + " (training)")
    print(str(round(testing_accuracy, 3)) + " (testing)")

    #
    # for alpha in range (1, 10):
    #     print("alpha = " + str(1.5 + alpha / 10))
    #     p_positive, p_negative, vocabulary = train(sys.argv[1], 1.5 + alpha / 10)
    #     testing_labels, testing_accuracy = test(sys.argv[2], p_positive, p_negative, vocabulary)
    #     print(testing_accuracy)



main()
