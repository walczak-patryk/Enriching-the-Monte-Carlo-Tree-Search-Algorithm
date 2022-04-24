import multiprocessing
import random
import time
import itertools
from ai.minmax import hex_evaluate, othello_evaluate
import tqdm
import numpy as np
from config import MCTS_ITERATIONS, MCTS_MAX_DEPTH

from games.hex.hex import Hex
from games.hive.hive import Hive
from games.hive.hive_evaluate import hive_evaluate
from games.othello.othello import Othello
from games.player import MCTS_Player, MCTSRAVE_Player, Random_Player, AlphaBeta_Player, MCTSStrategy_Player, MCTSSwitchingStrategy_Player
from games.othello.othello_player import MapBaseHeu_Othello_Player, Greedy_Othello_Player
from strategies.strategies import mobility_strategy, random_strategy
from test import Test

SEED = 22021070
REPETITIONS = 1
COMMON_PLAYERS = [MCTS_Player(max_depth=MCTS_MAX_DEPTH, number_of_iteration=MCTS_ITERATIONS), MCTSRAVE_Player(max_depth=MCTS_MAX_DEPTH, number_of_iteration=MCTS_ITERATIONS), Random_Player(), MCTSStrategy_Player(random_strategy, max_depth=MCTS_MAX_DEPTH, number_of_iteration=MCTS_ITERATIONS), MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy], max_depth=MCTS_MAX_DEPTH, number_of_iteration=MCTS_ITERATIONS)]
HIVE_PLAYERS = [AlphaBeta_Player(hive_evaluate)]
HEX_PLAYERS = [AlphaBeta_Player(hex_evaluate)]
OTHELLO_PLAYERS = [MapBaseHeu_Othello_Player(), Greedy_Othello_Player(), AlphaBeta_Player(othello_evaluate)]

def generate_instances(): 
    result = []

    # Othello, Hex, Hive
    game_types = [Othello, Hex, Hive]
    
    for r in itertools.product(game_types, COMMON_PLAYERS, COMMON_PLAYERS):
        for i in range(REPETITIONS):
            result.append(Test(r[0], r[1], r[2], seed = SEED + i))

    expeded_len = (len(COMMON_PLAYERS) * len(COMMON_PLAYERS) * len(game_types)) * REPETITIONS
    assert len(result) == expeded_len, f'Incorrect amount of test cases ({len(result)} != {expeded_len})'

    return result

def generate_specific_instances_hex(): 
    result = []
    
    for r in itertools.product(COMMON_PLAYERS, HEX_PLAYERS):
        for i in range(REPETITIONS):
            result.append(Test(Hex, r[0], r[1], seed = SEED + i))
            result.append(Test(Hex, r[1], r[0], seed = SEED + i))
    
    for r in itertools.product(HEX_PLAYERS, HEX_PLAYERS):
        for i in range(REPETITIONS):
            result.append(Test(Hex, r[0], r[1], seed = SEED + i))


    expeded_len = ((len(COMMON_PLAYERS) * len(HEX_PLAYERS) * 2) + (len(HEX_PLAYERS) * len(HEX_PLAYERS))) * REPETITIONS
    assert len(result) == expeded_len, f'Incorrect amount of hex test cases ({len(result)} != {expeded_len})'

    return result

def generate_specific_instances_hive(): 
    result = []
    
    for r in itertools.product(COMMON_PLAYERS, HIVE_PLAYERS):
        for i in range(REPETITIONS):
            result.append(Test(Hive, r[0], r[1], seed = SEED + i))
            result.append(Test(Hive, r[1], r[0], seed = SEED + i))

    for r in itertools.product(HIVE_PLAYERS, HIVE_PLAYERS):
        for i in range(REPETITIONS):
            result.append(Test(Hive, r[0], r[1], seed = SEED + i))


    expeded_len = ((len(COMMON_PLAYERS) * len(HIVE_PLAYERS) * 2) + (len(HIVE_PLAYERS) * len(HIVE_PLAYERS))) * REPETITIONS
    assert len(result) == expeded_len, f'Incorrect amount of hive test cases ({len(result)} != {expeded_len})'

    return result

def generate_specific_instances_othello(): 
    result = []
    
    for r in itertools.product(COMMON_PLAYERS, OTHELLO_PLAYERS):
        for i in range(REPETITIONS):
            result.append(Test(Othello, r[0], r[1], seed = SEED + i))
            result.append(Test(Othello, r[1], r[0], seed = SEED + i))

    for r in itertools.product(OTHELLO_PLAYERS, OTHELLO_PLAYERS):
        for i in range(REPETITIONS):
            result.append(Test(Othello, r[0], r[1], seed = SEED + i))

    expeded_len = ((len(COMMON_PLAYERS) * len(OTHELLO_PLAYERS) * 2) + (len(OTHELLO_PLAYERS) * len(OTHELLO_PLAYERS))) * REPETITIONS
    assert len(result) == expeded_len, f'Incorrect amount of othello test cases ({len(result)} != {expeded_len})'

    return result

def run_test(test):
    print(f'start of {test.name}')
    test.start()


def run_tests():
    iterable = generate_instances()
    iterable += generate_specific_instances_othello()
    iterable += generate_specific_instances_hex()
    iterable += generate_specific_instances_hive()

    # for i in iterable:
    #     run_test(i)

    random.shuffle(iterable)

    start_time = time.time()

    # run_test(iterable[0])

    max_cpu = multiprocessing.cpu_count()
    p = multiprocessing.Pool(int(max_cpu)-2)
    for _ in tqdm.tqdm(p.imap_unordered(run_test, iterable), total=len(iterable)):
        pass
    # p.map_async(run_test, iterable)
    p.close()
    p.join()

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    run_tests()
