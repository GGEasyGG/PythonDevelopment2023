import argparse
import random


def bullscows(guess, secret):
    nbulls, ncows = 0, 0

    for index, elem in enumerate(guess):
        if elem == secret[index]:
            nbulls += 1
        elif elem in secret:
            ncows += 1

    return nbulls, ncows


def gameplay(ask, inform, words):
    computer_word = random.choice(words)
    nattempts = 1

    user_word = ask('Введите слово: ', words)
    while user_word != computer_word:
        inform('Быки: {}, Коровы: {}', *bullscows(user_word, computer_word))
        nattempts += 1
        user_word = ask('Введите слово: ', words)

    return nattempts


def ask(prompt, valid=None):
    word = input(prompt)

    if valid is not None:
        while word not in valid:
            print('Введённого слова нет в словаре.')
            word = input(prompt)

    return word


def inform(format_string, bulls, cows):
    print(format_string.format(bulls, cows))




