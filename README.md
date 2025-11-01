# AI vs AI Survival Arena

A Pygame-based simulation showcasing three advanced AI algorithms competing in an autonomous survival arena with modern card-based UI and custom PNG assets.

## Overview

Watch two AI-controlled players compete against each other while navigating enemies, collecting resources, and making strategic decisions. This project demonstrates:

1. **A* Pathfinding** - Ally bots use optimal pathfinding to collect resources
2. **Minimax with Alpha-Beta Pruning** - Enemy agents choose optimal targets
3. **Fuzzy Logic** - AI players make strategic decisions based on game state

## Features

- **20×20 Grid Arena** - Visual battlefield with obstacles and resources
- **2 AI Players** - Blue Team vs Red Team, fully autonomous
- **4 Enemy Agents** - Attack players using Minimax algorithm
- **4 Ally Bots** - Collect resources using A* pathfinding (2 per team)
- **Dynamic Resources** - Health packs and coins spawn throughout the game
- **Modern UI Design** - Card-based layout with real-time stats and AI decision display
- **Custom PNG Assets** - Professional game graphics for entities, UI icons, and legends
- **Real-time Visualization** - Watch AI decisions unfold in Pygame GUI

## Requirements

- Python 3.7+
- Pygame

## Installation

```bash
# Install Pygame
pip install pygame

# Or using pip3
pip3 install pygame
```

## How to Run

```bash
cd survival_arena
python3 main.py
```

## Controls

- **SPACE** - Pause/Resume game
- **R** - Restart game
- **Q/ESC** - Quit
- **UP/DOWN** - Increase/Decrease game speed
- **D** - Toggle debug mode (shows AI paths)

## Game Rules

### Win Conditions
- First to reach **500 points** wins
- Survive while opponent is eliminated
- Highest score after **50 turns**

### Entities

**AI Players (Blue & Red)**
- Start with 100 HP
- Make decisions using Fuzzy Logic
- Actions: Collect resources, flee enemies, aggressive play, defensive play

**Ally Bots**
- Navigate using A* pathfinding
- Collect resources for their team
- 2 allies per player

**Enemy Agents**
- Choose targets using Minimax algorithm
- Deal 20 damage on contact
- 4 enemies total

**Resources**
- Health Packs: Restore 25 HP
- Coins: Worth 50 points
- Spawn randomly during gameplay

## AI Algorithms Explained

### 1. A* Pathfinding (Ally Bots)
- Uses Manhattan distance heuristic
- Finds optimal path avoiding obstacles
- Efficiently navigates to nearest resources

### 2. Minimax with Alpha-Beta Pruning (Enemies)
- Evaluates both players as potential targets
- Predicts player escape routes
- Optimizes targeting with depth-3 search
- Alpha-beta pruning reduces computation

### 3. Fuzzy Logic (AI Players)
- **Inputs**: health, score, enemy distance, resource distance
- **Outputs**: Strategic actions
- **Rules**:
  - Low health + near enemy → Flee
  - Low health + far enemy → Seek health
  - High health + low score → Collect coins
  - High health + high score → Aggressive play
  - Medium health → Defensive play

## Project Structure

```
survival_arena/
├── main.py                 # Entry point and game loop
├── game.py                 # Main game logic and state management
├── entities.py             # Entity classes (Player, Ally, Enemy, Resource)
├── rendering.py            # Pygame visualization with modern UI
├── assets.py               # PNG asset loader and manager
├── constants.py            # Game configuration and constants
├── ai/
│   ├── __init__.py
│   ├── astar.py           # A* pathfinding implementation
│   ├── minimax.py         # Minimax with alpha-beta pruning
│   └── fuzzy_logic.py     # Fuzzy decision system
├── icons/
│   ├── entities/          # Game entity PNG assets (30×30px)
│   ├── ui/                # UI icon assets (20×20px)
│   └── legend/            # Legend icon assets (16×16px)
└── figures/               # Documentation figures
```

## Technical Details

### Game Configuration
- Grid: 20×20 cells
- Window: 1400×900 pixels (modern widescreen layout)
- Grid Display: 700×700 pixels
- Sidebar: 630 pixels wide
- FPS: 5 (slower for better AI observation)
- Max Enemies: 4
- Max Obstacles: 30
- Max Resources: 6 health packs + 6 coins

### AI Parameters
- Minimax search depth: 3 levels
- Fuzzy membership functions: Triangular and Trapezoidal
- A* heuristic: Manhattan distance

## Watch the AI in Action

The game runs completely autonomously - no player input needed! Watch as:

- **Blue and Red players** analyze game state and make strategic decisions
- **Ally bots** efficiently pathfind to collect resources for their team
- **Enemy agents** dynamically switch targets based on opportunity
- **Complex behaviors** emerge from simple AI rules

## Success Criteria

✅ Autonomous AI vs AI gameplay
✅ Real-time visualization of all AI decisions
✅ Three distinct AI algorithms working together
✅ Strategic decision-making and pathfinding
✅ Dynamic resource management and combat
✅ Clear winner determination

## Educational Value

This project demonstrates:
- Search algorithms (A*)
- Game theory (Minimax)
- Fuzzy logic systems
- AI decision-making
- Game state management
- Real-time visualization
- Turn-based gameplay mechanics

## Contributor
Bishal Roy
2007098
CSE,KUET

Iqbal Mahamud
2007093
CSE,KUET

## License

This is an educational project demonstrating AI algorithms in game development.

---

**Enjoy watching the AIs battle it out!**
