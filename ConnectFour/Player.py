"""
Name: Jiaqi Duan

Notes:

Important for the project:
    1. Create sucessor states for a given state
    2. Assign values to those, if it's a terminal state
       --> if you've reached your maximum depth
       --> if one of the player wins
    3. Start with a fixed maximum depth value (3), add that property to the class, such as self.maxDepth
       and increment your current depth everytime you recurse in minimax tree. When you hit your maxDepth, 
       call your utility function to calculate the value of whatever board state you've created that represent it  
    4. Have a heuristic that only rewards possible winning moves

For get_move functions:
    1. Each of the move functions should return an index for the column the player make a move on

Alpha-beta functions:
    Max -> Min -> Max (calculate utilities, return max values)
    Calculate the utilities and get the minimum moves
    1. Start as max node, in order to maximize its utility
    2. Need to create successors for the state and iterate through those
    3. Need to calculate again the utility value for those successors
    4. Implement alpha-beta prunning and updating the value

Helper functions for Alpha-beta and Expectimax:
    1. Successors_helper_function:
        a) Sucessor is a board with updated values in it to represent making a move in a given column
           --> successor is the potential moves (7 copies of the board, each with the possible moves)
        b) There will have seven different successor states for the board 
        c) When creating successor states, be sure to create a copy of your board as you're doing it, 
           because you don't want to mainipulating the same object multiple times under the hood, and 
           it can get messy and you'll have successors that have multiple different moves that you've 
           put into them once

    2. Utility_helper_function:
        a) To calculate the utilities, set a value counter for pieces, such that when there's 3 pieces lining up, 
           value is maximum or when have the opportunity of lining up as 4 and when there's no pieces lining up 
           it's the lowest (set the value counter each time by checking) 
        b) Assign some sort of utility values to these intermediate states that represent how close you possibly 
           are to getting a connect four
        c) Look at game_completed function as a hint

References: Infinity values: https://www.geeksforgeeks.org/python-infinity/ 
"""

import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.maxDepth = 3 # this is the maximum depth

    def game_completed_helper_function(self, board, player_num):
        # this creates a string of player_num in a row
        # so if the player_num is 1 then it will create 1111
        player_win_str = '{0}{0}{0}{0}'.format(player_num) 

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

    # check this afterwards
    def successors_helper_function(self, board, player_number):
        """
            Successor helper functions for Alpha-beta and Expectimax:
                a) Sucessor is a board with updated values in it to represent making a move in a given column
                b) There will have seven different successor states for the board 
                c) When creating successor states, be sure to create a copy of your board as you're doing it, 
                because you don't want to mainipulating the same object multiple times under the hood, and 
                it can get messy and you'll have successors that have multiple different moves that you've 
                put into them once
        """
        successor_list = []
        # successor index list that represent the column index of that successor
        successor_index_list = []
        for j in range(board.shape[1]):
            new_board = board.copy()
            # iterate backwards
            for i in range(board.shape[0]-1, -1, -1):
                if new_board[i,j] == 0:   
                    new_board[i,j] = player_number
                    # j -> successor index list
                    successor_index_list.append(j)
                    break
            successor_list.append(new_board)
        # tuple with two lists
        return successor_list, successor_index_list

    def utility_helper_function(self, board, num_of_player_num, player_number):
        utility_list = []
        to_str = lambda a: ''.join(a.astype(str))
        num_of_player_num_in_str = '{0}' * num_of_player_num
        potential_player_win_str = num_of_player_num_in_str.format(player_number)

        def check_horizontal(b):
            count = 0
            # iterate through the first axis of your array
            for row in b:
                if potential_player_win_str in to_str(row):
                    count = count + to_str(row).count(potential_player_win_str)
            return count

        def check_verticle(b):
            return check_horizontal(b.T)

        def check_diagonal(b):
            count = 0
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                root_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if potential_player_win_str in to_str(root_diag):
                    count = count + to_str(root_diag).count(potential_player_win_str)

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = to_str(diag.astype(np.int))
                        if potential_player_win_str in diag:
                            count = count + diag.count(potential_player_win_str)
            return count

        utility_list.append(check_horizontal(board))
        utility_list.append(check_verticle(board))
        utility_list.append(check_diagonal(board))
        return sum(utility_list)
    
    def get_alpha_beta_move(self, board):
        
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        # dispatcher
        def value_alpha_beta(self, board, depth, alpha, beta, player_number):
            # flag counter for the MAX according to level
            if depth%2 == 0: MAX = True
            else: MAX = False
            # if the state is a terminal state (when the value reached the maximum depth or winning states met)
            # return the state's utiltiy
            if depth == self.maxDepth or self.game_completed_helper_function(board, player_number):
                return self.evaluation_function(board), None
            # if the next agent is MAX: return max_value(state)
            if MAX:
                # same thing in here for returning 
                max_value_f = max_value(self, board, depth, alpha, beta, player_number)
                # print(max_value_f)
                return max_value_f[0], max_value_f[1]
            # if the next agent is MIN: return min_value(state)
            else:
                min_value_f = min_value(self, board, depth, alpha, beta, player_number)
                return min_value_f[0], min_value_f[1]
            
        def max_value(self, board, depth, alpha, beta, player_number):
            # initialize v to -inf
            v = -np.inf
            move = 0
            # potential successor states
            potential_successors = self.successors_helper_function(board, player_number)[0]
            potential_successors_index = self.successors_helper_function(board, player_number)[1]
            # if the state is a terminal state (when the value reached the maximum depth or winning states met)
            # return the state's utiltiy
            if depth == self.maxDepth or self.game_completed_helper_function(board, player_number):
                return self.evaluation_function(board), None
            # for each successor of state:
            for i, successor in enumerate(potential_successors):
                ov = v
                v = max(v, value_alpha_beta(self, successor, depth+1, alpha, beta, player_number)[0])
                if ov != v and (i < len(potential_successors_index)):
                    move = potential_successors_index[i] 
                if v >= beta: return v, None
                alpha = max(alpha, v)
            return v, move
        
        def min_value(self, board, depth, alpha, beta, player_number):
            # initialize v to +inf
            v = np.inf
            move = 0
            # potential successor states
            potential_successors = self.successors_helper_function(board, player_number)[0]
            potential_successors_index = self.successors_helper_function(board, player_number)[1]
            # if the state is a terminal state (when the value reached the maximum depth or winning states met)
            # return the state's utiltiy
            if depth == self.maxDepth or self.game_completed_helper_function(board, player_number):
                return self.evaluation_function(board), None
            # for each successor state:
            for i, successor in enumerate(potential_successors):
                ov = v
                v = min(v, value_alpha_beta(self, successor, depth+1, alpha, beta, player_number)[0])
                # update move
                if ov != v and (i < len(potential_successors_index)):
                    move = potential_successors_index[i]
                if v <= alpha: return v, None
                beta = min(beta, v)
            return v, move
        
        # initializing the environment for alpha-beta 
        depth = 0
        alpha = -np.inf
        beta = np.inf
        return value_alpha_beta(self, board, depth, alpha, beta, self.player_number)[1]
        raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        # dispatcher
        # MAX as a boolean value, so True or False statements when calling
        def value_expectimax(self, board, depth, player_number):
            # flag counter for the MAX according to level
            if depth%2 == 0: MAX = True
            else: MAX = False
            # if the state is a terminal state (when the value reached the maximum depth or winning states met)
            # return the state's utiltiy
            if depth == self.maxDepth or self.game_completed_helper_function(board, player_number):
                return self.evaluation_function(board), None
            # if the next agent is MAX: return max_value(state)
            if MAX:
                max_value_f_1 = max_value(self, board, depth, player_number)
                return max_value_f_1[0], max_value_f_1[1]
            # if the next agent is EXP: return exp_value(state)
            else:
                exp_value_f = exp_value(self, board, depth, player_number)
                return exp_value_f[0], exp_value_f[1]
        
        def max_value(self, board, depth, player_number):
            # initialize v to -inf
            v = -np.inf
            move = 0
            # potential successor states
            potential_successors = self.successors_helper_function(board, player_number)[0]
            potential_successors_index = self.successors_helper_function(board, player_number)[1]
            # if the state is a terminal state (when the value reached the maximum depth or winning states met)
            # return the state's utiltiy
            if depth == self.maxDepth or self.game_completed_helper_function(board, player_number):
                return self.evaluation_function(board), None
            # for each successor of state:
            for i, successor in enumerate(potential_successors):
                ov = v
                v = max(v, value_expectimax(self, successor, depth+1, player_number)[0])
                # update move
                if ov != v and (i < len(potential_successors_index)):
                    # print(i) # 6
                    # print(len(potential_successors_index))
                    move = potential_successors_index[i] # 6
            return v, move
        
        def exp_value(self, board, depth, player_number):
            # initialize v to 0
            v = 0
            move = 0
            # potential successor states
            potential_successors = self.successors_helper_function(board, player_number)[0]
            potential_successors_index = self.successors_helper_function(board, player_number)[1] 
            # check if it's the terminal states
            if depth == self.maxDepth or self.game_completed_helper_function(board, player_number):
                return self.evaluation_function(board), None
            # for each successor state:
            for i, successor in enumerate(potential_successors):
                ov = v
                p = int(1/len(potential_successors))
                v += p * value_expectimax(self, successor, depth+1, player_number)[0]
                # update move
                if ov != v and (i < len(potential_successors_index)): 
                    move = potential_successors_index[i]
            return v, move

        depth = 0
        return value_expectimax(self, board, depth, self.player_number)[1]
        raise NotImplementedError('Whoops I don\'t know what to do')


    # for averaging the utilities for states
    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        player_number = self.player_number
        utility = 0
        if player_number == 1:
            opponent = 2
        else:
            opponent = 1

        # when the utility is higher, the more possible does the winner to win 
        utility = self.utility_helper_function(board, 3, player_number) * 1000
        utility += self.utility_helper_function(board, 2, player_number) * 100
        utility += self.utility_helper_function(board, 1, player_number) * 10

        return utility


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        # shape is a property of NumPy array, which reflects the dimensions
        # --> returns a list of dimension's length on it 
        # board.shape[1] will return 7 since board is a 6X7 NumPy array, and 2D NumPy array is [r][c]
        # print("Board before move: \n", board)
        for col in range(board.shape[1]):
            # looks through the board of the column
            # check if there's any zero in every row within the given column
            if 0 in board[:,col]: # [:] --> every value for that axis
                valid_cols.append(col)
        # print("Valid column after move: ", valid_cols)
        # returns a random value from a list of elements
        # choose a random move out of the random columns
        return np.random.choice(valid_cols)

class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

