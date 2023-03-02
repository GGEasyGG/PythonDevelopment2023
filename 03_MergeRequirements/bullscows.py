import argparse
import random
import sys
import validators
from urllib import request as req
import cowsay


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

    user_word = ask(f'Введите слово длиной {args.length}', words)
    while user_word != computer_word:
        inform('Быки: {}, Коровы: {}', *bullscows(user_word, computer_word))
        nattempts += 1
        user_word = ask(f'Введите слово длиной {args.length}', words)

    return nattempts


def ask(prompt, valid=None):
    cow = random.choice(cowsay.list_cows())
    word = input(cowsay.cowsay(prompt, cow=cow) + '\n\n')
    print()

    if valid is not None:
        while word not in valid:
            cow = random.choice(cowsay.list_cows())
            print(cowsay.cowsay('Введённого слова нет в словаре', cow=cow))
            print()
            word = input(cowsay.cowsay(prompt, cow=cow) + '\n\n')
            print()

    return word


def inform(format_string, bulls, cows):
    cow = random.choice(cowsay.list_cows())
    print(cowsay.cowsay(format_string.format(bulls, cows), cow=cow))
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dict', type=str)
    parser.add_argument('length', nargs='?', default=5, type=int)
    args = parser.parse_args()

    cow = random.choice(cowsay.list_cows())

    if validators.url(args.dict):
        with req.urlopen(args.dict) as file:
            dictionary = [line.strip() for line in file.read().decode().split('\n') if args.length == len(line.strip())]
    else:
        try:
            with open(args.dict, 'r') as file:
                dictionary = [line.strip() for line in file if args.length == len(line.strip())]
        except Exception as exc:
            print(exc)
            sys.exit()

    if not dictionary:
        print(cowsay.cowsay('Запустите игру с меньшей длиной слова', cow=cow))
        print()
        sys.exit()

    print(cowsay.cowsay(f'Вы угадали слово за {gameplay(ask, inform, dictionary)} попыток', cow=cow))
    print()
