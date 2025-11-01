# Quick Start Guide

## Installation

1. Make sure you have Python 3.7 or higher installed:
   ```bash
   python3 --version
   ```

2. Install Pygame:
   ```bash
   pip3 install pygame
   # Or
   pip3 install -r requirements.txt
   ```

## Running the Game

1. Navigate to the survival_arena directory:
   ```bash
   cd survival_arena
   ```

2. Run the game:
   ```bash
   python3 main.py
   ```

3. Watch the AI players compete!

## Running Tests

To verify everything is working:
```bash
cd survival_arena
python3 test_game.py
```

## What You'll See

- **Blue Team (top-left)** - AI player with light blue allies
- **Red Team (bottom-right)** - AI player with light red allies
- **Purple Triangles** - Enemy agents using Minimax
- **Green Circles with Cross** - Health packs (+25 HP)
- **Gold Circles with $** - Coins (+50 points)
- **Gray Squares** - Obstacles

## Game Controls

| Key | Action |
|-----|--------|
| SPACE | Pause/Resume |
| R | Restart game |
| Q or ESC | Quit |
| UP | Increase speed |
| DOWN | Decrease speed |
| D | Toggle debug mode |

## Understanding the AI

### Blue/Red Players (Fuzzy Logic)
Watch the "Action" display to see their current strategy:
- **Flee Enemy** - Low health, enemy nearby
- **Seek Health** - Low health, enemy far
- **Collect Coins** - Healthy, need points
- **Aggressive Play** - Healthy, high score, attacking
- **Defensive Play** - Balanced approach
- **Collect Resources** - General resource gathering

### Ally Bots (A* Pathfinding)
Small circles that efficiently navigate to the nearest resource using optimal pathfinding.

### Enemy Agents (Minimax)
Purple triangles that intelligently choose which player to target based on distance and health.

## Win Conditions

The game ends when:
1. A player reaches 500 points
2. A player's health reaches 0
3. 50 turns elapse (highest score wins)

## Tips for Watching

- **Increase speed** with UP key to see longer games faster
- **Pause** with SPACE to examine the current state
- Watch how players adapt their strategies based on health and score
- Notice how enemies switch targets based on opportunity
- Observe allies efficiently collecting resources

## Troubleshooting

**Game won't start:**
- Make sure Pygame is installed: `pip3 install pygame`
- Check Python version: `python3 --version` (needs 3.7+)

**Import errors:**
- Make sure you're in the survival_arena directory
- Run the test script: `python3 test_game.py`

**Performance issues:**
- Lower the FPS with DOWN key
- Close other applications

## Next Steps

After watching a few games:
- Try adjusting AI parameters in `constants.py`
- Modify fuzzy logic rules in `ai/fuzzy_logic.py`
- Change game balance (health, damage, resources)
- Add new features!

Enjoy the AI battle!
