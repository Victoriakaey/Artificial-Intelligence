--------------------------------------------------------   How to run the program   ----------------------------------------------------------

To run the code, write the following command in terminal after locating to the path of the file:

    ConnectFour.py [player1] [player2] --time [TIME]

where [player1] and [player2] could be human, ai, or random, and [TIME] is the value used to limit the amount of time in seconds to wait for the AI player to make a move. [TIME] is an optional argument, which has a default value of 60 seconds

For example, if I were to play the game using human as player1 and ai as player2, and set time constraint to be 5 seconds per turn, then I will do the following command:

    ConnectFour.py human ai --time 5
    
Or, if I don't want to set a time constraint to the AI player, I will simply just do:

    ConnectFour.py human ai
    
---------------------------------------------------------   About this program   ------------------------------------------------------------

1. Implement an AI agent to play the game Connect 4 against a human player (which will take user input move from terminal), a random player (which it will choose from valid columns with equal probability) or another AI player. 

2. The AI agent will use the Alpha-beta Search Algorithm and the Expectimax Search Algorithm to select the next move given the current board state. 

3. This is a depth-limited search game, where the max depth is set to be 3.

4. Analysis after running the program multiple times: If I do AI player vs. AI player, the player that goes first do better in general.

