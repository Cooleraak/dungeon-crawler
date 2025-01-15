# User Manual

---

#### _Welcom to the user manul! This manual explains the basic mechanics and gameplay of the game._

---

## How to Play

After opening `menu.py`, a menu will open. 

<img src="https://github.com/Cooleraak/dungeon-crawler/blob/main/docs/images/menu_screen.png" alt="legendary dungeon" width="300" height="300"/>

---

You can choose between 3 buttons: `NEW_GAME`, `LOAD` and `QUIT`
  -`NEW_GAME`: Start the game with a brand new character to play with
  -`LOAD`: Start the game with the character you played with previously (new if first game)
  -`QUIT`: Close the window

After picking either `NEW_GAME` or `LOAD`, the buttons disappear and you're thrown right in!

---

In front of you, there are `2 doors`, `an arrow` and a `QUIT` button. You can move by clicking one of the doors or the button. The button moves you into the previous room, the doors move you forward.

<img src="https://github.com/Cooleraak/dungeon-crawler/blob/main/game_assets/visual_assets/basic_room_sprite.png" alt="room" width="300" height="300"/>

---

There are many types of doors and rooms awaiting you:
 
### Room Types

`Explored`
 - If you've already been in a room, you will be shown via a checkmark
 - This is practically an empty room so entering it multiple times does nothing

<img src="https://github.com/Cooleraak/dungeon-crawler/blob/main/game_assets/visual_assets/already_explored_sprite.png" alt="already explored" width="150" height="300"/>

---

`?`
 - Contains either: `Basic Enemy` fight, `Basic reward` or `Nothing`

<img src="https://github.com/Cooleraak/dungeon-crawler/blob/main/game_assets/visual_assets/nothing_sprite.png" alt="?" width="150" height="300"/>

---

`Basic Enemy`
 - Contains a `Basic Enemy` fight that rewards small reward

<img src="https://github.com/Cooleraak/dungeon-crawler/blob/main/game_assets/visual_assets/basic_enemy_sprite.png" alt="Basic Enemy" width="150" height="300"/>

---

`Elite Enemy`
 - Contains a `Elite Enemy` fight that rewards medium reward

<img src="https://github.com/Cooleraak/dungeon-crawler/blob/main/game_assets/visual_assets/elite_enemy_sprite.png" alt="Elite Enemy" width="150" height="300"/>

---

`Reward`
 - Contains medium reward

<img src="https://github.com/Cooleraak/dungeon-crawler/blob/main/game_assets/visual_assets/reward_sprite.png" alt="Reward" width="150" height="300"/>

---

`Boss`
 - Contains a `Boss Enemy` fight that rewards large reward

<img src="https://github.com/Cooleraak/dungeon-crawler/blob/main/game_assets/visual_assets/boss_sprite.png" alt="Boss" width="150" height="300"/>

---

### Door Types

`Trap`
 - Hurts the player if walked through
 - Is destroyed after one use

<img src="https://github.com/Cooleraak/dungeon-crawler/blob/main/game_assets/visual_assets/trap_sprite.png" alt="Trap" width="150" height="300"/>

---

`Portal`
 - Acts as a doorway to a specific reward room on the map
 - All portals lead to the same room
 - Stays open forever

<img src="https://github.com/Cooleraak/dungeon-crawler/blob/main/game_assets/visual_assets/portal_sprite.png" alt="Portal" width="150" height="300"/>

---

`Wall`
 - Just a wall
 - Indicates end of map

<img src="https://github.com/Cooleraak/dungeon-crawler/blob/main/game_assets/visual_assets/wall_sprite.png" alt="Wall" width="150" height="300"/>

---

## How to Fight

When a `Fight` begins, an enemy will appear on the screen and you must beat it before traversing further.
You can see `ENEMY` health and their mana above their head.
You can see `PLAYER` health, mana and potion count in the bottom left corner of the screen along with new buttons.

You and the enemy take turns, each having one action per turn (bosses get an extra action each turn)

While in a fight, the combat buttons become available:
 - `ATK` - use 50 `mana` to strike an enemy with an attack; costs a turn
 - `SKILL` - use 100 `mana` to strike an enemy with an empowered attack; costs a turn
 - `ITEM` - recover `health` based on level; does NOT cost a turn
 - `MANA` - recover 50 `mana`; costs a turn

<img src="https://github.com/Cooleraak/dungeon-crawler/blob/main/docs/images/fight_screen.png" alt="combat screen" width="300" height="300"/>

## Goals

Every time you start a game, one of 3 random goals will be chosen.
The goals are:
 - `explore` - visit 85% of the map
 - `execute` - defeat all enemies on the map
 - `boss` - defeat a boss

Your current goal as well as a tracker and combat log will show up in the terminal log

<img src="https://github.com/Cooleraak/dungeon-crawler/blob/main/docs/images/status.png" alt="status log" width="300" height="300"/>

After completing the set goal, a message will pop up in the terminal log and the game will close, needing to be reopened again for another round.

