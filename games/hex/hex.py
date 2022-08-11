from copy import deepcopy
import sys
import os

from config import BOARD_SIZE

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from games.game import Game
from games.hex.const import BLUE_PLAYER, RED_PLAYER
from games.player import Player

from games.hex.logic import Logic
from games.hex.ui import UI

# from mcts import MCTS


class Hex(Game):
    def __init__(self, player1:Player, player2:Player, use_ui: bool = False, board_size: int = BOARD_SIZE):
        self.name = f"Hex{board_size}"
        
        # Mode
        self.player1=player1
        self.player2=player2
        self.turn_state = 1

        use_ui = use_ui or player1.is_man or player2.is_man

        # Instantiate classes
        self.use_ui = use_ui
        self.ui = None
        if use_ui:
            pygame.init()
            pygame.display.set_caption("Hex")
            self.ui = UI(board_size)
        self.logic = Logic(self.ui, board_size)
        self.board_size = board_size

        # Initialize variables
        self.node = None
        self.winner = 0
        self.turn_state = BLUE_PLAYER
        
    def restart(self):
        self.turn_state = 1
        self.logic = Logic(self.ui, self.board_size)

        # Initialize variables
        self.node = None
        self.winner = 0
        self.turn_state = BLUE_PLAYER

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP or not (self.player1.is_man or self.player2.is_man):
                return True
        return False

    def check_move(self, move, player):
        # Forbid playing on already busy node
        try:
            self.winner = self.logic.check_and_make_action(player, move)
            # if self.winner:
            #     print('win')
        except AssertionError:
            print("invalid move")
            return False

        return True

    def player_make_move(self, player, node = None):
        if player.is_man:
            if node is None:
                return None
            args = (self.ui, node)
        else:
            args = (self.logic.logger, self.turn_state, self.get_result, self.get_all_posible_moves, self.change_player, self.board_move, None)
            
        move = player.make_move(args)
        return move

    def end_condition(self):
        return self.winner

    def swich_player(self):
        # Next turn
        if self.turn_state == 1:
            self.turn_state = 2
            return self.player2
        else:
            self.turn_state = 1
            return self.player1

    def get_winner(self):
        if self.winner:
            # print("Player {} wins!".format(self.winner))
            return True

    def play_with_ui(self):
        # print(f'{self.name} starts')
        node = None
        current_player = self.player1
        while not self.end_condition():
            # dist_board = self.logic.manhattan_distance(self.logic.logger, self.turn_state)
            # self.ui.draw_board(dist_board)
            self.ui.draw_board()
    
            if current_player.is_man:
                node = self.ui.get_node_hover()
                         
            pygame.display.update()
            self.ui.clock.tick(30)

            cliced = self.handle_events()

            if (current_player.is_man and cliced) or not current_player.is_man:
                move = self.player_make_move(current_player, node)
                if self.check_move(move, self.turn_state):  
                    current_player = self.swich_player()  
        self.ui.draw_board()
        pygame.display.update()
        self.get_winner()
        print(f"Player {self.winner} wins!")
        self.wait_for_click()

       

        return self.winner
    
    def play_without_ui(self):
        # print(f'{self.name} starts')
        current_player = self.player1
        while not self.end_condition():
            # move = current_player.make_move()
            move = self.player_make_move(current_player)
            self.check_move(move, self.turn_state)
            current_player = self.swich_player()

        self.get_winner()
        return self.winner

    def get_result(self, state, player) -> int:
        result = self.logic.is_game_over(player, state, False)
        if result is None:
            result = 0.5
        return result

    def get_all_posible_moves(self, iteration_state, player = None) -> list:
        v = self.logic.is_game_over(None, iteration_state, False, False)
        if self.logic.is_game_over(None, iteration_state, False, False):
            return []
        else:
            moves = self.logic.get_possible_moves(iteration_state)
            return moves

    def change_player(self, player) -> int:
        if player == 2:
            return 1
        else:
            return 2

    def board_move(self, state, move, player):
        (x, y) = move

        # assert self.logic.is_node_free((x, y), state), "node is busy"
        if self.logic.logger[x][y] : raise("node is busy")
        state[x][y] = player
        return state

        
