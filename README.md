# Shifting_stones_engine

An interactive CLI game engine for the popular tactical card game "Shifting Stones" built using Python data structures and object oriented programming with state encapsulation and random/probabilistic card pattern and grid tile generation.

## Game rules

To fully understand the code and the algorithms implemented in it , I highly recommend reading through the rules of the game first:
https://www.64ouncegames.com/pages/shifting-stones

## Game Engine Workflow

1. The 4 players and the 3x3 grid tile pattern is intialised with a randomised pattern while adhering to the tile count contraints set by the rules of the game.
2. A validated tiered deck is created and for the first round 4 cards each is dealt to the players.
3. After every move of a player the cards in their hand and the current state of the grid is displayed.
4. Each turn allows the user to input one of the few different "moves" like swap, flip, score etc. while expeding a card that is pushed to the discard pile list     and the hand is refilled upto 4 cards from the deck and the turn is ended.
5. While scoring the pattern on the card ID the user inputs is compared to the grid state and validated and then the points are awarded if any.
6. The game action loop goes on until the "endgame trigger" i.e, until a player reaches 8 cards scored (tracked at every turn for each player), once the endgame     is triggered,  the loop goes for one last turn to other players then terminates and at last displays the final scores of each player along with the winner.

## Architecture and Structural Flow
### Objects (eg. Card, Stone, Player etc)
1. Stone: Encapsulates a dual-sided state tracker by assigning each side 1 or 0 as index. It uses a 1-x modifier to "flip" the stone i.e change the state from
          0 to 1 or 1 to 0 in a single operation.
2. Card: Houses coordinate dictionaries mapping the grid coordinates to certain colors to form a pattern and also stores the point value if the card is scored.
         The card is displayed as a pattern in the 3x3 2D matrix in the console along with its cardID and the points value.
3. Player: It tracks basic scalar variables like name, score, cards_scored_count, and a boolean flag (has_skipped_last_turn) to enforce turn rules. It also holds            a hand list containing active Card objects.
4. ShiftingStones: This is the master controller class that coordinates the entire application, manages the rules, and orchestrates the other objects. It holds                      the overall game state, including a nested 2D list matrix representing the 3x3 grid of Stone objects, a deck list of Card objects, a                              discard_pile list, and an active player index tracking pointer. It contains background logic methods like _create_structured_deck(), which                        runs loops to dynamically generate randomized card configurations while using conditional filters (_is_valid_pattern) to ensure no illegal                        cards are created.It provides system methods like verify_pattern_match(), swap_stones(), and check_endgame_condition() that cross-reference                       player coordinates against the 2D grid layout to approve moves and update scores.

## NOTE
1. This is strictly a 4 player variant of the original game.
2. The card patterns in the randomly generated deck are very specific and involve the whole grid which is a slight deviation from the original card game, since      there do exist card patter which are row/column flexible. eg. This engine only validates a row of say R G W in the 1st row alone, but the orignal card game       may validate the same combination of colors in any row.
3. The row,column input given by the user must be 0 indexed and NOT 1 indexed.


