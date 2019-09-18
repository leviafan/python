""" Generator function for "rock-scissors-paper-lizard-spock"
"""
import random


def player():
    while True:
        yield random.randrange(0, 5)


if __name__ == '__main__':
    a = []
    b = player()
    for i in range(10):
        a.append(next(b))

    print(a)
