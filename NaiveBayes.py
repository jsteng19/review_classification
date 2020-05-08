import math

def classify(train, test, alpha):
    file = open(train)

    p_count, n_count = 0, 0
    p_dict, n_dict = {}, {}
    for line in file:
        text, classification = line.rsplit(",")
        words = text.split()
        # words = set(text.split())
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

    ## inital attempt -- 58%
    # p_probabilities = {word: math.log((p_dict[word] + alpha) / (p_dict[word] + n_dict[word] + alpha * len(vocabulary)))
    #                    for word in vocabulary}
    #
    # n_probabilities = {word: math.log((n_dict[word] + alpha) / (p_dict[word] + n_dict[word] + alpha * len(vocabulary)))
    #                    for word in vocabulary}

    p_probabilities = {word: math.log((p_dict[word] + alpha) / (p_word_sum + alpha * len(vocabulary)))
                       for word in vocabulary}

    n_probabilities = {word: math.log((n_dict[word] + alpha) / (n_word_sum + alpha * len(vocabulary)))
                       for word in vocabulary}

    # p_probabilities = {word: math.log((p_dict[word] + alpha * (p_dict[word] + n_dict[word]) / (p_word_sum + n_word_sum)) / (p_word_sum + alpha))
    #                    for word in vocabulary}
    #
    # n_probabilities = {word: math.log((n_dict[word] + alpha * (p_dict[word] + n_dict[word]) / (p_word_sum + n_word_sum)) / (n_word_sum + alpha))
    #                     for word in vocabulary}

    # p_probabilities = { word: math.log((p_dict[word] + 1) / (p_word_sum + p_dict[word] + n_dict[word]))
    #                     for word in vocabulary}
    #
    # n_probabilities = { word: math.log((n_dict[word] + 1) / (n_word_sum + p_dict[word] + n_dict[word]))
    #                     for word in vocabulary}

    p_bias = math.log(p_count / (p_count + n_count))
    n_bias = math.log(n_count / (p_count + n_count))

    file = open(test)

    linecount, correctcount = 0, 0
    for line in file:
        text, classification = line.rsplit(",")
        words = text.split()
        positive, negative = 0, 0
        for word in words:
            if word in vocabulary:
                positive += p_probabilities[word]
                negative += n_probabilities[word]
        if classification == "0\n":
            if negative > positive: correctcount += 1
        else:
            if positive > negative: correctcount += 1

        linecount += 1

    print("accuracy: " + str(correctcount / linecount))



def main():
    classify("training.txt", "testing.txt", 2)
    # for alpha in range (1, 10):
    #     print("alpha = " + str(alpha))
    #     classify("training.txt", "testing.txt", alpha)




main()
