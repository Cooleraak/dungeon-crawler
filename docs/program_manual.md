# Program manual

#### _Welcome to the program manual! This manual explains the program's external and internal structure and the algorithm for computer movement._

---
## Files and their classes

1. `game_logic.py`:
    - exploration_logic - keeps track of game state for map, exploration goal and player
    
    - encounter_logic - contains all the methods needed to start and enact a battle

2. `map_layout_gen`:
    - game_map_generation - generates and composes the game map

3. `map_contents_gen`:
    - `room_setup` - generates contents of rooms such as enemies or loot

4. `player`:
    - `player` - used as representation of the player in-game

    - `save_data` - saves the relevaant player data into save.txt

    - `load_data` - loads data from save.txt

    - `construct_player_data` - constructs player with either base data or loaded data

5. `enemy_assets`:
    - `enemy_tiers` - used as a list for enemy tiers through a dictionary

    - `enemy_action_properties` - describes what attacks each enemy has through a dictionary

    - `enemy_stat_properties` - describes the hp and damage of each enemy through a dictionary

    - `enemy_attacks` - describes potency of aattacks through a dictionary

6. `legendary_dungeon`:
    - `button` - used to construct buttons

    - `game` - contains the main game loop with exploration and battle loop

7. `menu`:
    - `menu` - contains the game menu

8. `save`:
    - contains the saved data for player

## methods

`class exploration_logic` - methods that initialize exploration_logic are omitted

    - set_completion_goal() - randomly chooses a goal for current playthrough

    - check_for_EOE(tree, player) - checks for end of exploration, meaning if the goal is completed

    - update_exploration_status(tree) - updates the status of current goal

    - combat_end(node, player) - creates loot for current room and updates player xp

---
`class encounter_logic` - methods that initialize encounter_logic are omitted

    - `start_battle(player_move)` - enacts a single turn cycle (player-enemy-enemy); uses best_move() to decide a move for computer

    - `calculalte_dmg(actor, move)` - calculates total damage of used movement

    - `make_move(actor, move, is_testing)` - updates hp and mp based on move used and passives of actors

    - `best_move(first_action_of_round)` - finds the best move for computer by comparing scores of all possible moves

    - `minimax(curr_depth, enemy_turn, first_action_of_round)` - simulates battle to decide the best course of action for computer

    - `score_calculator()` - evaluates score for current state of actors

    - `check_for_EOC(is_testing)` - checks if combat ended

---
`class game_map_generation` - methods that initialize game_map_generation are omitted

    - subclass `Node` - node of a binary tree

    - generate_map() - starts map generation and returns starting point

    - generate_node(curr_depth, node_data, parent = None) - creates a node, sets its type, and connects it to parent and child nodes

    - choose_node_type() - chooses a node type to give to a node

---
`class room_setup` - methods that initialize room_setup are omitted

    - sub-class `chest` - used as representation of loot in-game

    - sub-class `enemy_char` - used as representation of enemies in-game

    - enemy_generation() - constructs enemy_char for current enemy

    - loot_generation() - constructs chest for current loot

    - set_room_tier() - appoints a room with a tiers

---
`class player` - methods that initialize player are omitted

    - update_xp() - updates the player`s xp and level

---
`class load_data` - methods that initialize load_data are omitted

    - get_level() - returns saved level from file

    - get_item() - returns saved item count form file

    - get_xp() - returns saved xp from file

---
`class construct_player_data` - methods that initialize construct_player_data are omitted

    - construct(load) - returns constructed player

    - curr_level() - returns current level either from load or basic

    - curr_moveset(level) - returns moveset based on current level

    - curr_passives(level) - returns passives based on current level

    - curr_item() - returns current item count either from load or basic

    - curr_xp() - returns current xp either from load or basic

---
`class button` - methods that initialize button are omitted

    - draw(surface) - draws the button on screen

    - is_clicked(mouse_pos) - checks if button was is_clicked

---
`class game`

    - __init__(start, player) - constructor; creates main game window and starts main game loop

    - encounter_on_screen_load(player_char) - main combat loop and checks for combat button clicked

    - exploration_on_screen_load() - updates the screen on room entrance and checks for exploration button clicked

---
`class menu`

    - __init__() - constructor; creates menu window and checks for menu button clicked


## Computer's algorithm
```
The computer uses Minimax algorithm and calculates 3 turns ahead during combat
```
### What's Minimax algorithm?
```
- it's a recursive algorithm typically used in two-player games where players take turns (e.g. chess, tic-tac-toe).
- the goal is to find the optimal move for the computer assuming that the player is also playing optimally.
- the algorithm builds a tree of possible game states and evaluates them to determine the best move.
- the evaluation is trying to maximize the score for the computer and minimize for the player. 
```
### How does the Minimax algorithm work?
```
- The algorithm builds a tree based on the current game state.

- Based on current actor, the Minimax algorithm:
    1. Simulates all of the actor's moves on copies of the actors
    2. Repeats for the next actor in queue until maximum depth is reached
    3. Returns scores for each move
```
### How is the score calculated?
```
After every move simulation, the score for the current state gets calculated based on current actors' hp and mp.
The best_move() function then compares all the moves' scores and returns the move with best score for the computer.
```