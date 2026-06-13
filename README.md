# Shifting_stones_engine

An interactive CLI game engine for the popular tactical card game "Shifting Stones" built using Python data structures and object oriented programming with state encapsulation and random/probabilistic card pattern and grid tile generation.

## Game rules

To fully understand the code and the algorithms implemented in it , I highly recommend reading through the rules of the game first:
https://www.64ouncegames.com/pages/shifting-stones

## Game Engine Workflow

1. The 4 players and the 3x3 grid tile pattern is intialised with a randomised pattern while adhering to the tile count contraints set by the rules of the game.
2. A validated tiered deck is created and for the first round 4 cards each is dealt to the players.
3. After every move of a player the cards in their hand and the current state of the grid is displayed.
4. Each turn allows the user to input one of the few different "moves" like swap, flip, score etc. while expeding a card that is pushed to the discard pile list and
   the hand is refilled upto 4 cards from the deck and the turn is ended.
5. While scoring the pattern on the card ID the user inputs is compared to the grid state and validated and then the points are awarded if any.
6. The game action loop goes on until the "endgame trigger" i.e, until a player reaches 8 cards scored (tracked at every turn for each player), once the endgame is
   triggered,  the loop goes for one last turn to other players then terminates and at last displays the final scores of each player along with the winner.

## Architecture and Structural Flow
### Objects (eg. Card, Stone, Player etc)
1. Stone: Encapsulates a dual-sided state tracker using a $1 - x$ index modifier map to toggle between underlying string representations seamlessly when a player commits to a flip command.
2. Card: Houses coordinate dictionaries mapping absolute grid offsets `(r, c)` to expected target colors, combined with automated string text wrapping for clean console matrix rendering.

The system entities—Stone, Card, and Player—act as autonomous, encapsulated classes responsible for maintaining their own local state attributes; for instance, each Stone object tracks its visible face value using an index modifier to mutate state via a discrete flip() method, while each Card object maps static geometric coordinates to target colors using dictionary key-value pairs. Orchestrating these components is the ShiftingStones structural manager, which acts as the primary controller.


