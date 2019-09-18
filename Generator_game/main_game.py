import player_logic
import time
import os
from typing import List, Callable, Tuple

# win_conditions[a][b] == 1 indicates that a beats b
# and win_conditions[b][a] == 1 means that b beats a
# [Rock, Scissors, Paper, Lizard, Spock]
win_conditions = [
    [-1, 1, 0, 1, 0],
    [0, -1, 1, 1, 0],
    [1, 0, -1, 0, 1],
    [0, 0, 1, -1, 1],
    [1, 1, 0, 0, -1]
]

move_symbols = ['()', '8<', '[]', '~:', '-Y']
players_num = 16


def game_round(first, second) -> Tuple[int, int, int]:
    first_choice, second_choice = next(first), next(second)
    while first_choice == second_choice:
        first_choice, second_choice = next(first), next(second)
# in this form we get index of winner. 0 - first, 1 - second
    winner_index = win_conditions[second_choice][first_choice]

    return (winner_index, first_choice, second_choice)


def redraw_table(lines: List[str]):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    for line in lines:
        print(line)


if __name__ == '__main__':

    players: List = []
    player_strings: List[str] = []
    pl_idx: List[int] = []

    for idx in range(players_num):
        players.append(player_logic.player())
        player_strings.append(' ' * (5 - len(str(idx))) + f'{str(idx)}:')
        pl_idx.append(idx)

    players_in_round = players_num

    redraw_table(player_strings)

    while players_in_round > 1:
        time.sleep(1)

        for idx in range(players_in_round, 0, -2):
            (winner, first_ch, second_ch) = game_round(
                players[idx - 1],
                players[idx - 2]
            )
            player_strings[pl_idx[idx - 1]] += f' -- {move_symbols[first_ch]} '
            player_strings[pl_idx[idx - 2]] += f' -- {move_symbols[second_ch]} '

            players.pop(idx + winner - 2).close()
            pl_idx.pop(idx + winner - 2)

        redraw_table(player_strings)

        players_in_round //= 2

    print(f'\n\nThe winner is {pl_idx[0]}!')
