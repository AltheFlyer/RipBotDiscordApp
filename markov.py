import random
import re

START_OF_LINE = " "
END_OF_LINE = "  "

# Markov table and wordlist, preinitialized with start and end of line values
words = [START_OF_LINE, END_OF_LINE]
markov_table = [[0, 0], [0, 0]]
# Used to easily generate random numbers based on number of references a word has
sum_array = [0, 0]


def add_word(previous, word):
    # Remove lead/trail whitespace

    if previous:
        previous = previous.strip()
    else:
        previous = START_OF_LINE

    if word:
        word = word.strip()
    else:
        word = END_OF_LINE

    # print(previous + " " + word)

    # Get current number of words
    length = len(words)

    # print(markov_table)
    # Expand table if new word is introduced
    if word not in words:
        # Columns

        for y in range(length):
            markov_table[y].append(0)
        markov_table.append([])
        # New row
        for x in range(length + 1):
            markov_table[length].append(0)

        # print(markov_table)
        words.append(word)
        sum_array.append(0)

    # Add to markov
    previous_index = words.index(previous)
    word_index = words.index(word)
    # for the previous word, increase the number of linkings to the next by 1
    markov_table[previous_index][word_index] += 1
    # increase stored sum for the previous word
    sum_array[previous_index] += 1

    # print(markov_table)


def generate_next(word, count):
    # an attempt at not ending things abruptly
    if count <= 0 or word == END_OF_LINE:
        if random.randrange(0, 19) < count:
            return "\n" + generate_next(" ", count - 5)
        return ""
    # get index of word in list
    word_index = words.index(word)
    # if theres no linkings, send in some generic response (I hope this never runs)
    if sum_array[word_index] == 0:
        return "<done>"
    # generate random number based on sum of weightings for the next word
    r = random.randrange(0, sum_array[word_index])
    # find which word is chosen by weight
    carry = sum_array[word_index]
    for i in range(len(sum_array) - 1, -1, -1):
        if r >= carry - markov_table[word_index][i]:
            return words[i] + " " + generate_next(words[i], count - 1)
        else:
            carry -= markov_table[word_index][i]


def generate():
    return generate_next(" ", 20)

