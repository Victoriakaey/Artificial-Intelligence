# system libs
import argparse
import multiprocessing as mp
import tkinter as tk

# 3rd party libs
import numpy as np

# Local libs
from Player import AIPlayer, RandomPlayer, HumanPlayer

#https://stackoverflow.com/a/37737985
def turn_worker(board, send_end, p_func):
    send_end.send(p_func(board))


class Game:
    def __init__(self, player1, player2, time):
        self.players = [player1, player2]
        self.colors = ['yellow', 'red']
        self.current_turn = 0
        self.board = np.zeros([6,7]).astype(np.uint8)
        self.gui_board = []
        self.game_over = False
        self.ai_turn_limit = time

        #https://stackoverflow.com/a/38159672
        root = tk.Tk()
        root.title('Connect 4')
        self.player_string = tk.Label(root, text=player1.player_string)
        self.player_string.pack()
        self.c = tk.Canvas(root, width=700, height=600)
        self.c.pack()

        for row in range(0, 700, 100):
            column = []
            for col in range(0, 700, 100):
                column.append(self.c.create_oval(row, col, row+100, col+100, fill=''))
            self.gui_board.append(column)

        tk.Button(root, text='Next Move', command=self.make_move).pack()

        root.mainloop()

    def make_move(self):
        if not self.game_over:
            current_player = self.players[self.current_turn]

            if current_player.type == 'ai':
                
                if self.players[int(not self.current_turn)].type == 'random':
                    p_func = current_player.get_expectimax_move
                else:
                    p_func = current_player.get_alpha_beta_move
                
                try:
                    recv_end, send_end = mp.Pipe(False)
                    p = mp.Process(target=turn_worker, args=(self.board, send_end, p_func))
                    p.start()
                    if p.join(self.ai_turn_limit) is None and p.is_alive():
                        p.terminate()
                        raise Exception('Player Exceeded time limit')
                except Exception as e:
                    uh_oh = 'Uh oh.... something is wrong with Player {}'
                    print(uh_oh.format(current_player.player_number))
                    print(e)
                    raise Exception('Game Over')

                move = recv_end.recv()
            else:
                move = current_player.get_move(self.board)

            if move is not None:
                self.update_board(int(move), current_player.player_number)

            if self.game_completed(current_player.player_number):
                self.game_over = True
                self.player_string.configure(text=self.players[self.current_turn].player_string + ' wins!')
            else:
                self.current_turn = int(not self.current_turn)
                self.player_string.configure(text=self.players[self.current_turn].player_string)

    # places that move at the lowest possible index
    # Therefore, you don't need to worry about placing a move in a 
    # specific index in the array, you just need to return the column number
    # for the move you want to make
    def update_board(self, move, player_num):
        # reference link: https://www.w3schools.com/python/numpy/numpy_array_slicing.asp
        # [:,index_num] means slicing from index_num to form a new numpy array
        if 0 in self.board[:,move]:
            update_row = -1
            for row in range(1, self.board.shape[0]):
                update_row = -1
                if self.board[row, move] > 0 and self.board[row-1, move] == 0:
                    update_row = row-1
                elif row==self.board.shape[0]-1 and self.board[row, move] == 0:
                    update_row = row

                if update_row >= 0:
                    self.board[update_row, move] = player_num
                    self.c.itemconfig(self.gui_board[move][update_row],
                                      fill=self.colors[self.current_turn])
                    break
        else:
            err = 'Invalid move by player {}. Column {}'.format(player_num, move)
            raise Exception(err)


    def game_completed(self, player_num):
        # this creates a string of player_num in a row
        # so if the player_num is 1 then it will create 1111
        player_win_str = '{0}{0}{0}{0}'.format(player_num) 

        board = self.board
        # it joins all the elements of that row and turn it into a string
        to_str = lambda a: ''.join(a.astype(str)) # lambda function check

        def check_horizontal(b):
            # iterate through the first axis of your array
            for row in b:
                if player_win_str in to_str(row):
                    return True
            return False

        def check_verticle(b):
            # calls check_horizontal in the transpose of b
            return check_horizontal(b.T)

        def check_diagonal(b):
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if player_win_str in to_str(root_diag):
                    return True

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if player_win_str in diag:
                            return True

            return False

        return (check_horizontal(board) or
                check_verticle(board) or
                check_diagonal(board))



def main(player1, player2, time):
    """
    Creates player objects based on the string paramters that are passed
    to it and calls play_game()

    INPUTS:
    player1 - a string ['ai', 'random', 'human']
    player2 - a string ['ai', 'random', 'human']
    """
    def make_player(name, num):
        if name=='ai':
            return AIPlayer(num)
        elif name=='random':
            return RandomPlayer(num)
        elif name=='human':
            return HumanPlayer(num)

    Game(make_player(player1, 1), make_player(player2, 2), time)


def play_game(player1, player2):
    """
    Creates a new game GUI and plays a game using the two players passed in.

    INPUTS:
    - player1 an object of type AIPlayer, RandomPlayer, or HumanPlayer
    - player2 an object of type AIPlayer, RandomPlayer, or HumanPlayer

    RETURNS:
    None
    """
    board = np.zeros([6,7])



if __name__=='__main__':
    player_types = ['ai', 'random', 'human']
    parser = argparse.ArgumentParser()
    parser.add_argument('player1', choices=player_types)
    parser.add_argument('player2', choices=player_types)
    parser.add_argument('--time',
                        type=int,
                        default=60,
                        help='Time to wait for a move in seconds (int)')
    args = parser.parse_args()

    main(args.player1, args.player2, args.time)
