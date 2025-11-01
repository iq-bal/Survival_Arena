# Game Logic Documentation - AI vs AI Survival Arena

## Table of Contents
1. [Game Overview](#game-overview)
2. [Game Initialization](#game-initialization)
3. [Turn Execution Flow](#turn-execution-flow)
4. [Entity Behaviors](#entity-behaviors)
5. [AI Decision Systems](#ai-decision-systems)
6. [Collision Detection](#collision-detection)
7. [Resource Management](#resource-management)
8. [Win/Loss Conditions](#winloss-conditions)
9. [Game Scenarios](#game-scenarios)
10. [Edge Cases](#edge-cases)

---

## Game Overview

The AI vs AI Survival Arena is a turn-based strategy game where two AI-controlled players compete on a 20×20 grid battlefield. Each player commands a team consisting of:
- 1 AI Player (decision-maker)
- 2 Ally Bots (resource collectors)

They compete against:
- 4 Enemy Agents (hostile entities)
- 30 Static Obstacles (walls)

The objective is to reach 500 points first or survive 50 turns with the highest score.

---

## Game Initialization

### 1. Arena Setup (game.py:49-108)

**Obstacle Generation:**
```
1. Generate 30 random positions on the 20×20 grid
2. Create Obstacle entities at these positions
3. Store obstacle positions for pathfinding algorithms
```

**Player Placement:**
```
1. Blue Player spawns near position (2, 2) - top-left corner
2. Red Player spawns near position (17, 17) - bottom-right corner
3. Both avoid obstacle positions
4. Starting health: 100 HP each
5. Starting score: 0 points each
```

**Ally Bot Placement:**
```
Blue Team Allies:
  - Ally 1: Near position (1, 2)
  - Ally 2: Near position (2, 1)

Red Team Allies:
  - Ally 3: Near position (18, 17)
  - Ally 4: Near position (17, 18)

All avoid obstacles and existing entity positions
```

**Enemy Placement:**
```
1. 4 enemies spawn near center position (10, 10)
2. Avoid all occupied positions
3. Each enemy has no initial target
```

**Initial Resources:**
```
Health Packs: 6 spawned randomly
Coins: 6 spawned randomly
All avoid occupied positions and obstacles
```

---

## Turn Execution Flow

### Complete Turn Sequence (game.py:217-247)

Each turn executes in the following order:

```
1. Player 1 AI Decision & Movement
   ├─ Evaluate game state using Fuzzy Logic
   ├─ Choose action (FLEE, SEEK_HEALTH, COLLECT_COINS, etc.)
   ├─ Calculate target position
   └─ Move using A* pathfinding

2. Player 2 AI Decision & Movement
   ├─ Evaluate game state using Fuzzy Logic
   ├─ Choose action (FLEE, SEEK_HEALTH, COLLECT_COINS, etc.)
   ├─ Calculate target position
   └─ Move using A* pathfinding

3. Update All Allies
   ├─ For each ally:
   │   ├─ Find nearest uncollected resource
   │   ├─ Calculate path using A*
   │   └─ Move one step toward resource

4. Update All Enemies
   ├─ For each enemy:
   │   ├─ Use Minimax algorithm to choose target
   │   ├─ Evaluate both players
   │   ├─ Choose optimal target and move
   │   └─ Move one step toward target

5. Check All Collisions
   ├─ Player-Enemy collisions → Apply damage
   ├─ Player-Resource collisions → Collect
   ├─ Ally-Resource collisions → Collect for owner
   └─ Player-Player collision → Both take damage

6. Spawn New Resources
   ├─ 15% chance to spawn health pack
   └─ 15% chance to spawn coin

7. Increment Turn Counter

8. Check Game Over Conditions
   ├─ Score threshold reached?
   ├─ Player eliminated?
   └─ Maximum turns reached?
```

---

## Entity Behaviors

### 1. AI Players (entities.py:8-48)

**Attributes:**
- Position: (x, y) on grid
- Team: "Blue" or "Red"
- Health: 0-100 HP
- Score: 0-∞ points
- Decision State: Current AI action
- Alive: Boolean status

**Behaviors:**
- **Move:** Controlled by Fuzzy Logic decisions + A* pathfinding
- **Take Damage:** Reduce health, die if health ≤ 0
- **Heal:** Increase health up to 100 HP max
- **Score:** Accumulate points from coins

**Movement Pattern:**
```
Each turn:
1. Fuzzy Logic analyzes: health, score, enemy distance, resource distance
2. Outputs action: FLEE_ENEMY, SEEK_HEALTH, COLLECT_COINS, etc.
3. Determines target position based on action
4. A* calculates path avoiding obstacles
5. Moves one step toward target
```

---

### 2. Ally Bots (entities.py:51-73)

**Attributes:**
- Position: (x, y)
- Owner: Reference to player
- Target Resource: Current collection goal

**Behaviors:**
- **Resource Detection:** Find nearest uncollected resource (health or coin)
- **Pathfinding:** Use A* to navigate to resource
- **Collection:** When reaching resource, owner receives benefit
- **No Combat:** Allies cannot fight or take damage

**Movement Algorithm (game.py:295-315):**
```
For each ally:
1. Scan all resources on map
2. Filter out collected resources
3. Calculate Manhattan distance to each
4. Select nearest resource
5. Use A* to find path
6. Move one step along path
```

---

### 3. Enemy Agents (entities.py:76-97)

**Attributes:**
- Position: (x, y)
- Target Player: Current attack target
- Target Position: Destination

**Behaviors:**
- **Target Selection:** Use Minimax algorithm to choose best target
- **Chasing:** Move toward chosen player
- **Damage Dealing:** Deal 20 HP damage on contact
- **Tactical Switching:** Change targets based on opportunity

**Decision Algorithm (game.py:317-347):**
```
If both players alive:
  1. Run Minimax with depth 3
  2. Evaluate attacking Player 1 vs Player 2
  3. Consider player health, distance, escape routes
  4. Choose target with maximum value
  5. Move one step using A* toward target

If only one player alive:
  1. Chase surviving player
  2. Move one step using A*
```

---

### 4. Resources (entities.py:100-139)

**Types:**

**Health Pack:**
- Visual: Green cross icon
- Effect: Restore 25 HP
- Max: 6 on map simultaneously
- Value: Crucial for survival

**Coin:**
- Visual: Yellow circle with $ symbol
- Effect: Add 50 points to score
- Max: 6 on map simultaneously
- Value: Required for score victory

**Collection Mechanism:**
```
1. Entity (player or ally) moves to resource position
2. Collision detected in _check_collisions()
3. resource.collect(player) is called
4. If health pack: player.heal(25)
5. If coin: player.add_score(50)
6. Resource marked as collected
7. Resource becomes invisible but not removed
```

---

### 5. Obstacles (entities.py:142-157)

**Attributes:**
- Position: (x, y)
- Static: Never moves

**Behavior:**
- Block all entity movement
- Included in pathfinding obstacle set
- Force entities to navigate around them

---

## AI Decision Systems

### 1. Fuzzy Logic (ai/fuzzy_logic.py)

**Purpose:** Strategic decision-making for AI players

**Inputs:**
1. **Health (0-100)**
   - LOW: 0-35 HP
   - MEDIUM: 30-70 HP
   - HIGH: 65-100 HP

2. **Score (0-500)**
   - LOW: 0-200 points
   - MEDIUM: 150-350 points
   - HIGH: 300-500 points

3. **Enemy Distance (0-20 cells)**
   - NEAR: 0-4 cells
   - MEDIUM: 3-8 cells
   - FAR: 7-20 cells

4. **Resource Distance (0-20 cells)**
   - NEAR: 0-4 cells
   - MEDIUM: 3-8 cells
   - FAR: 7-20 cells

**Membership Functions:**

**Triangular (fuzzy_logic.py:13-33):**
```
      1.0 |    /\
          |   /  \
          |  /    \
      0.0 |_/______\_____
          left peak right
```

**Trapezoidal (fuzzy_logic.py:36-57):**
```
      1.0 |   ____
          |  /    \
          | /      \
      0.0 |/________\___
          left l_peak r_peak right
```

**Fuzzy Rules (fuzzy_logic.py:105-192):**

```
Rule 1: IF health LOW AND enemy NEAR
        THEN FLEE_ENEMY (priority: 1.5×)

Rule 2: IF health LOW AND enemy FAR
        THEN SEEK_HEALTH

Rule 3: IF health HIGH AND score LOW
        THEN COLLECT_COINS

Rule 4: IF health HIGH AND score HIGH
        THEN AGGRESSIVE_PLAY

Rule 5: IF health MEDIUM
        THEN DEFENSIVE_PLAY

Rule 6: IF health LOW AND enemy MEDIUM
        THEN COLLECT_RESOURCES (cautious)

Rule 7: IF health MEDIUM AND score LOW
        THEN COLLECT_RESOURCES

Rule 8: IF enemy NEAR AND health MEDIUM
        THEN DEFENSIVE_PLAY (priority: 1.2×)
```

**Defuzzification:**
```
1. Calculate strength for each rule
2. Use MAX operator for action aggregation
3. Select action with maximum strength
4. Return action string (e.g., "FLEE_ENEMY")
```

**Output Actions:**
- `FLEE_ENEMY`: Move away from nearest enemy
- `SEEK_HEALTH`: Navigate to nearest health pack
- `COLLECT_COINS`: Navigate to nearest coin
- `COLLECT_RESOURCES`: Navigate to any nearest resource
- `AGGRESSIVE_PLAY`: Chase opponent player
- `DEFENSIVE_PLAY`: Balanced resource collection

---

### 2. A* Pathfinding (ai/astar.py)

**Purpose:** Optimal path calculation for allies and player movement

**Algorithm Steps:**

```
1. Initialize:
   - Open set: [start position]
   - Closed set: []
   - g_score: {start: 0}
   - f_score: {start: h(start, goal)}

2. While open set not empty:
   a. Select node with lowest f_score
   b. If node == goal: reconstruct path, return
   c. Move node from open to closed
   d. For each neighbor:
      - Skip if obstacle or out of bounds
      - Skip if in closed set
      - Calculate tentative g_score
      - If better path found:
        * Update g_score and f_score
        * Add to open set
        * Record parent for path reconstruction

3. If open set empty: no path exists, return [start]
```

**Heuristic Function (astar.py:15-18):**
```python
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
```

**Next Move Selection (astar.py:70-80):**
```
1. Calculate complete path from current to target
2. If path found and length > 1:
   - Return second position in path (next step)
3. Else:
   - Return current position (stay in place)
```

---

### 3. Minimax with Alpha-Beta Pruning (ai/minimax.py)

**Purpose:** Optimal target selection for enemy agents

**Algorithm Structure:**

```
Minimax Tree (depth 3):

Level 0 (MAX - Enemy choosing target):
├─ Option A: Attack Player 1
│  └─ Level 1 (MIN - Player 1 escapes):
│     ├─ Move Up
│     ├─ Move Down
│     ├─ Move Left
│     └─ Move Right
│        └─ Level 2 (MAX - Enemy chases):
│           ├─ Move toward P1
│           └─ ...
│              └─ Level 3: Evaluate position
│
└─ Option B: Attack Player 2
   └─ Level 1 (MIN - Player 2 escapes):
      └─ ...
```

**Evaluation Function (minimax.py:71-97):**

```
Score = Distance_to_Target × (-1)
      + Player_Health × (-0.1)
      + (20 - Distance) × 10  (proximity bonus)
```

**Goal:** Maximize enemy advantage (lower health, closer distance)

**Alpha-Beta Pruning:**
```
1. Alpha: Best value for MAX player (enemy)
2. Beta: Best value for MIN player (human players)
3. If Beta ≤ Alpha at any node:
   - Prune remaining branches
   - Skip evaluation (optimization)
```

**Target Selection (minimax.py:100-146):**

```
1. Evaluate attacking Player 1:
   - Run minimax from enemy position toward P1
   - Get score for this choice

2. Evaluate attacking Player 2:
   - Run minimax from enemy position toward P2
   - Get score for this choice

3. Choose target with higher score

4. Calculate next move toward chosen target using A*

5. Return (target_position, next_move)
```

---

## Collision Detection

### Collision Check System (game.py:349-380)

**1. Player-Enemy Collision:**
```
For each enemy:
  If player1.alive AND enemy.position == player1.position:
    player1.take_damage(20)

  If player2.alive AND enemy.position == player2.position:
    player2.take_damage(20)

Effect:
- Player loses 20 HP immediately
- If health ≤ 0: player.alive = False
- Game checks for elimination victory
```

**2. Player-Resource Collision:**
```
For each resource (not collected):
  If player1.alive AND resource.position == player1.position:
    resource.collect(player1)

  If player2.alive AND resource.position == player2.position:
    resource.collect(player2)

Effect (Health Pack):
- Player health += 25 HP (capped at 100)
- Resource marked collected

Effect (Coin):
- Player score += 50 points
- Resource marked collected
- Game checks for score victory
```

**3. Ally-Resource Collision:**
```
For each ally:
  For each resource (not collected):
    If ally.position == resource.position:
      resource.collect(ally.owner)  # Owner gets benefit!

Effect:
- Ally's owner (player) receives resource benefit
- Allies act as remote resource collectors
```

**4. Player-Player Collision:**
```
If player1.alive AND player2.alive AND
   player1.position == player2.position:
  player1.take_damage(10)
  player2.take_damage(10)

Effect:
- Both players lose 10 HP
- Discourages direct confrontation
- Forces tactical positioning
```

---

## Resource Management

### Dynamic Resource Spawning (game.py:181-216)

**Spawn Mechanism:**

```
Each turn after collision resolution:

1. Health Pack Spawning:
   - Check: random() < 0.15 (15% chance)
   - Count current health packs (not collected)
   - If count < 6:
     * Find free position
     * Spawn new health pack
     * Add to resources list

2. Coin Spawning:
   - Check: random() < 0.15 (15% chance)
   - Count current coins (not collected)
   - If count < 6:
     * Find free position
     * Spawn new coin
     * Add to resources list
```

**Free Position Algorithm (game.py:124-150):**
```
1. Generate random position (x, y)
2. Check occupied positions:
   - Obstacles
   - Players
   - Allies
   - Enemies
   - Existing resources (not collected)
3. If position free: return position
4. Else: try nearby positions in expanding radius
5. Last resort: scan entire grid
```

**Resource Lifecycle:**
```
1. SPAWNED:
   - Created at random position
   - collected = False
   - Visible on map

2. COLLECTED:
   - Entity touches resource
   - Benefit applied to player
   - collected = True
   - Invisible on map (still in list)

3. REPLACED:
   - New resource spawns elsewhere
   - Old collected resources remain in memory
   - Only uncollected resources count toward limit
```

---

## Win/Loss Conditions

### Game Over Scenarios (game.py:447-498)

**1. Score Victory:**
```
Check every turn:
  If player1.score >= 500:
    Winner: Blue Team
    Reason: "Blue Team wins by score!"

  If player2.score >= 500:
    Winner: Red Team
    Reason: "Red Team wins by score!"

Requirements:
- First to reach 500 points
- Each coin worth 50 points → need 10 coins minimum
- Faster collection = faster victory
```

**2. Elimination Victory:**
```
Check every turn:
  If NOT player1.alive AND player2.alive:
    Winner: Red Team
    Reason: "Red Team wins by survival!"

  If NOT player2.alive AND player1.alive:
    Winner: Blue Team
    Reason: "Blue Team wins by survival!"

Causes of Death:
- Health drops to 0 or below
- Multiple enemy attacks (20 HP each)
- Player collision damage (10 HP each)
- Failure to collect health packs
```

**3. Draw by Double Elimination:**
```
Check every turn:
  If NOT player1.alive AND NOT player2.alive:
    Winner: None
    Reason: "Draw! Both players eliminated!"

Rare scenario:
- Both players die in same turn
- Usually from player-player collision at low health
- Or simultaneous enemy attacks
```

**4. Time Limit Victory:**
```
Check every turn:
  If turn_count >= 50:
    If player1.score > player2.score:
      Winner: Blue Team
      Reason: "Blue Team wins by score after 50 turns!"

    Else If player2.score > player1.score:
      Winner: Red Team
      Reason: "Red Team wins by score after 50 turns!"

    Else:
      Winner: None
      Reason: "Draw after 50 turns!"

Strategic Implications:
- Aggressive coin collection important
- Survival becomes crucial near turn 50
- Defensive play can force time limit
```

---

## Game Scenarios

### Scenario 1: Early Game Rush

**Setup:**
- Turn: 1-15
- Health: Both players near 100 HP
- Score: Both players 0-100 points

**Typical Behavior:**

**Blue Player:**
```
1. Fuzzy logic: health HIGH, score LOW
2. Action: COLLECT_COINS
3. Navigates to nearest coin
4. Allies also collecting resources
5. Avoids enemies (distance usually >5)
```

**Red Player:**
```
1. Fuzzy logic: health HIGH, score LOW
2. Action: COLLECT_COINS
3. Navigates to nearest coin
4. Allies also collecting resources
5. Avoids enemies (distance usually >5)
```

**Enemies:**
```
1. Minimax evaluates both players
2. Choose target with better opportunity
3. Start moving from center toward players
4. Haven't reached players yet (distance ~8-10)
```

**Outcome:**
- Both players accumulate 50-150 points
- No significant health loss
- Resource competition begins

---

### Scenario 2: Enemy Engagement

**Setup:**
- Turn: 15-30
- Health: 60-100 HP
- Score: 100-250 points
- Enemies closing in (distance 2-5)

**Critical Decision Point:**

**Player with health 80 HP, enemy at distance 3:**
```
Fuzzy Logic:
- health: 80 → HIGH membership = 0.75
- enemy_dist: 3 → NEAR membership = 0.67
- score: 150 → MEDIUM membership = 1.0

Rule 8: IF enemy NEAR AND health MEDIUM → DEFENSIVE_PLAY (strength: 0.67 × 1.2)
Rule 4: IF health HIGH AND score MEDIUM → mixed action (strength: 0.75 × 0.5)

Result: DEFENSIVE_PLAY wins
Action: Collect resources while maintaining distance from enemies
```

**Player with health 30 HP, enemy at distance 2:**
```
Fuzzy Logic:
- health: 30 → LOW membership = 1.0
- enemy_dist: 2 → NEAR membership = 1.0
- score: 200 → MEDIUM membership = 1.0

Rule 1: IF health LOW AND enemy NEAR → FLEE_ENEMY (strength: 1.0 × 1.5 = 1.5)

Result: FLEE_ENEMY wins (highest priority)
Action: Move away from nearest enemy
Target: Opposite corner from enemy
```

**Outcome:**
- Low health players flee to corners
- Healthy players continue resource collection
- Enemy successfully applies pressure
- Health pack collection becomes critical

---

### Scenario 3: Critical Health

**Setup:**
- Turn: 20-40
- Blue Health: 25 HP
- Red Health: 80 HP
- Blue Score: 300 points
- Red Score: 200 points

**Blue Player Behavior:**
```
Fuzzy Logic Analysis:
- health: 25 → LOW membership = 1.0
- nearest_enemy_dist: 6 → MEDIUM membership = 0.67
- nearest_health_dist: 4 → NEAR membership = 0.5

Rule 2: IF health LOW AND enemy FAR → SEEK_HEALTH (strength: 0.0, enemy not far)
Rule 6: IF health LOW AND enemy MEDIUM → COLLECT_RESOURCES (strength: 0.67 × 0.7)

Decision: COLLECT_RESOURCES (prioritize health packs)
Target: Nearest health pack at distance 4
Path: A* calculates safe route avoiding enemies

Turn N: Move toward health pack (24 HP if hit by enemy)
Turn N+1: Reach health pack → health = 25 + 25 = 50 HP
Turn N+2: Fuzzy logic: health MEDIUM → DEFENSIVE_PLAY
```

**Red Player Behavior:**
```
Fuzzy Logic Analysis:
- health: 80 → HIGH membership = 0.75
- score: 200 → LOW membership = 0.6
- nearest_coin_dist: 3 → NEAR membership = 1.0

Rule 3: IF health HIGH AND score LOW → COLLECT_COINS (strength: 0.6)

Decision: COLLECT_COINS
Target: Nearest coin at distance 3

Outcome: Red collects coin → 250 points
         Blue survives critical moment
```

---

### Scenario 4: Final Sprint

**Setup:**
- Turn: 40-50
- Blue: 450 points, 60 HP
- Red: 400 points, 70 HP
- 1 coin remaining on map

**Blue Player:**
```
Fuzzy Logic:
- health: 60 → MEDIUM membership = 0.8, HIGH membership = 0.25
- score: 450 → HIGH membership = 0.75
- nearest_coin_dist: 5 → MEDIUM membership = 0.67

Rule 4: IF health HIGH AND score HIGH → AGGRESSIVE_PLAY (strength: 0.25 × 0.75)
Rule 7: IF health MEDIUM AND score LOW → mixed (strength: 0.0)

Decision: AGGRESSIVE_PLAY (actually targets coin since score not quite won)
Path: Straight line to coin
Distance: 5 cells = 5 turns

Turn 45: Distance 4
Turn 46: Distance 3
Turn 47: Distance 2
Turn 48: Distance 1
Turn 49: Collect coin! → 450 + 50 = 500 points
WINNER: Blue Team wins by score!
```

**Red Player:**
```
Same coin target, but distance 7:
Turn 45: Distance 6
Turn 46: Distance 5
Turn 47: Distance 4
Turn 48: Distance 3
Turn 49: Distance 2
Turn 50: Would collect, but Blue already won!

Alternative: If turn 50 reached with Blue at 450, Red at 450:
Result: "Draw after 50 turns!"
```

---

### Scenario 5: Aggressive Play Backfire

**Setup:**
- Turn: 25
- Both players: 100 HP, 300 points
- Collision: Player positions become same

**Before Collision:**
```
Blue at (10, 10), health 100
Red at (11, 10), health 100

Blue decision: AGGRESSIVE_PLAY → target Red position
Red decision: AGGRESSIVE_PLAY → target Blue position

Blue moves right: (10, 10) → (11, 10)
Red moves left: (11, 10) → (10, 10)  [planned before Blue moved]
```

**After Movement Update:**
```
Both players now at (10, 10) - same position!
Collision detection triggers:
  player1.take_damage(10) → Blue: 90 HP
  player2.take_damage(10) → Red: 90 HP

Next turn fuzzy logic:
- Both health: 90 → HIGH membership = 1.0
- Both reconsider aggressive play
- Likely switch to DEFENSIVE_PLAY or resource collection
```

**Outcome:**
- Aggressive play is risky
- Health loss without enemy involvement
- Forces tactical spacing
- Benefits: closer to resources possibly

---

### Scenario 6: Ally Bot Efficiency

**Setup:**
- Turn: 10
- Blue player focusing on coins (COLLECT_COINS)
- Blue allies have different targets

**Entity Positions:**
```
Blue Player: (5, 5) → targeting coin at (8, 8)
Blue Ally 1: (4, 5) → finds health pack at (6, 3)
Blue Ally 2: (5, 4) → finds coin at (3, 7)

Resources visible:
- Coin at (8, 8) - distance 6 from player
- Health pack at (6, 3) - distance 4 from ally 1
- Coin at (3, 7) - distance 4 from ally 2
```

**Turn 10:**
```
Player moves (5,5) → (6,6) toward (8,8)
Ally 1 moves (4,5) → (5,4) toward (6,3) health pack
Ally 2 moves (5,4) → (4,5) toward (3,7) coin
```

**Turn 12:**
```
Ally 1 reaches (6,3) - collects health pack
  → Blue player health 85 → 100 HP (was 85)

Ally 2 reaches (3,7) - collects coin
  → Blue player score 150 → 200 points

Player still moving toward (8,8)
```

**Outcome:**
- Allies provide massive advantage
- Heal players remotely
- Accelerate score accumulation
- Allow player to focus on strategy
- 3× resource collection rate per team

---

### Scenario 7: Minimax Target Switching

**Setup:**
- Enemy at (10, 10)
- Blue player at (8, 12) with 100 HP
- Red player at (15, 10) with 30 HP

**Minimax Evaluation:**

```
Option A: Attack Blue Player
  Distance: |10-8| + |10-12| = 2 + 2 = 4
  Evaluation: -4 + (-100 × 0.1) + (20-4) × 10
            = -4 - 10 + 160
            = 146

Option B: Attack Red Player
  Distance: |10-15| + |10-10| = 5 + 0 = 5
  Evaluation: -5 + (-30 × 0.1) + (20-5) × 10
            = -5 - 3 + 150
            = 142

Decision: Attack Blue (score 146 > 142)
Reason: Closer distance outweighs lower health
```

**Next Turn - Red heals to 55 HP:**

```
Option A: Attack Blue
  Distance: 3 (enemy moved closer)
  Evaluation: -3 + (-100 × 0.1) + (20-3) × 10
            = -3 - 10 + 170
            = 157

Option B: Attack Red
  Distance: 4
  Evaluation: -4 + (-55 × 0.1) + (20-4) × 10
            = -4 - 5.5 + 160
            = 150.5

Decision: Still attack Blue (157 > 150.5)
```

**Turn After - Blue flees to (5, 15):**

```
Option A: Attack Blue
  Distance: |10-5| + |10-15| = 5 + 5 = 10
  Evaluation: -10 + (-100 × 0.1) + (20-10) × 10
            = -10 - 10 + 100
            = 80

Option B: Attack Red
  Distance: 3 (now closer)
  Evaluation: -3 + (-55 × 0.1) + (20-3) × 10
            = -3 - 5.5 + 170
            = 161.5

Decision: SWITCH to Red (161.5 > 80)
Reason: Blue fled too far, Red became better opportunity
```

**Outcome:**
- Enemies dynamically switch targets
- Prioritize closer, weaker players
- Fleeing can redirect enemy attention
- Creates tactical opportunities

---

## Edge Cases

### Edge Case 1: No Valid Path

**Scenario:**
```
Player at (5, 5) surrounded by obstacles:
  (4,5) = wall
  (6,5) = wall
  (5,4) = wall
  (5,6) = wall

Target: Coin at (10, 10)
```

**A* Pathfinding Result:**
```
1. Open set eventually becomes empty
2. No path found to (10, 10)
3. Return [current_position]
4. Player stays at (5, 5)

Next Turn:
- Fuzzy logic may switch to different action
- Try different target
- Or wait for dynamic resource spawn nearby
```

**Resolution:**
- Player not permanently stuck
- Game continues
- Other entities (enemies, allies) still move
- New resources may spawn in accessible areas

---

### Edge Case 2: All Resources Collected

**Scenario:**
```
Turn 30:
- All 6 health packs collected
- All 6 coins collected
- No uncollected resources on map
```

**Player Behavior:**
```
Fuzzy decision: COLLECT_COINS
Target calculation: _get_nearest_resource_position()
  - Scans all resources
  - Finds none with collected=False
  - Returns current_position (fallback)

Result: Player stays in place for one turn

Next Turn Resource Spawn:
- 15% chance × 2 = ~30% chance at least one resource spawns
- If spawned: Players resume movement
- If not: Players stay still another turn
```

**Outcome:**
- Temporary stalemate
- Resources will eventually spawn (probability)
- Enemies still move and attack
- Forces defensive positioning

---

### Edge Case 3: Exact Simultaneous Victory

**Scenario:**
```
Turn 45:
Blue score: 450, Red score: 450

Turn 46:
- Blue collects coin → 500 points
- Red collects coin → 500 points (same turn)
```

**Code Execution:**
```
check_game_over() called at turn end:

Line 450: if self.player1.score >= 500:
  → True! Blue reached 500
  → Set winner = player1
  → Set reason = "Blue Team wins by score!"
  → return (exit function)

Line 456: if self.player2.score >= 500:
  → Never evaluated! Function already returned
```

**Result:**
```
Winner: Blue Team
Reason: Player 1 checked first in code
```

**Note:**
- Code favors Blue Team in exact ties
- Rare scenario (requires precise timing)
- Could be randomized in future version

---

### Edge Case 4: Player Spawns on Resource

**Scenario:**
```
Initial setup:
- _spawn_resources() called
- Random position generated: (2, 2)
- Player1 position: (2, 2)
```

**Occupied Position Check:**
```
Line 155: occupied = obstacle_positions | {self.player1.position, self.player2.position}
Line 162: pos = self._find_free_position(..., occupied)

_find_free_position checks:
- If (2,2) in occupied → True
- Tries nearby positions in expanding radius
- Returns (2,3) or (3,2) instead
```

**Result:**
- Resource never spawns on player
- Always finds alternative position
- No immediate collision on game start

---

### Edge Case 5: Enemy Targets Dead Player

**Scenario:**
```
Turn 35:
- Blue player dies (health = 0)
- Enemy 1 was targeting Blue
```

**Next Turn Enemy Update:**
```
Line 321: if self.player1.alive and self.player2.alive:
  → False! (player1 not alive)
  → Skip Minimax evaluation

Line 341: elif self.player2.alive:
  → True! Only Red alive
  → enemy.target_position = self.player2.position
  → Calculate path using A*
  → All enemies now chase Red
```

**Result:**
- Enemies immediately switch to surviving player
- No wasted turns targeting dead player
- Increases pressure on survivor
- Makes elimination victory harder to maintain

---

### Edge Case 6: Fuzzy Logic Tie

**Scenario:**
```
Player health: 50 HP (exactly medium)
Enemy distance: 5 (exactly medium)
Score: 250 (exactly medium)
```

**Fuzzy Evaluation:**
```
Rule 5: IF health MEDIUM → DEFENSIVE_PLAY (strength: 1.0)
Rule 7: IF health MEDIUM AND score MEDIUM → COLLECT_RESOURCES (strength: 1.0)

Both rules have strength 1.0!

max(action_strengths, key=action_strengths.get)
  → Returns first action with max value in dictionary order
  → DEFENSIVE_PLAY (appears first in dictionary)
```

**Result:**
- Tie-breaking is deterministic
- Based on dictionary insertion order
- DEFENSIVE_PLAY typically wins ties
- Consistent behavior, not random

---

### Edge Case 7: Grid Boundary Movement

**Scenario:**
```
Player at (0, 0) - top-left corner
Enemy at (1, 1)
Fuzzy decision: FLEE_ENEMY
```

**Flee Calculation (game.py:413-445):**
```
dx = 0 - 1 = -1
dy = 0 - 1 = -1

Normalize: dx = -1, dy = 0 (prefer horizontal)

Target flee position:
x = max(0, min(19, 0 + (-1) × 3)) = max(0, min(19, -3)) = 0
y = max(0, min(19, 0 + 0 × 3)) = 0

Flee target: (0, 0) - same position!
```

**A* Pathfinding:**
```
Path from (0,0) to (0,0) = [(0,0)]
Next move: current position
Result: Player doesn't move
```

**Outcome:**
- Corner trapping possible
- Player stuck when enemies nearby
- Health decreases each turn (20 HP per hit)
- Death occurs without health packs
- Strategic importance of avoiding corners

---

### Edge Case 8: Ally Bot Priority Conflict

**Scenario:**
```
Blue Ally 1 at (5, 5) - targeting coin at (7, 7)
Blue Ally 2 at (5, 6) - also finds coin at (7, 7) is nearest

Turn N:
- Both allies move toward (7,7)
- Ally 1 moves to (6,6)
- Ally 2 moves to (6,7)

Turn N+1:
- Ally 1 moves to (7,7) - COLLECTS COIN
  → coin.collected = True
  → Blue player gets 50 points

- Ally 2 still targeting (7,7)
  → Moves to (7,7)
  → Collision check: coin already collected
  → No effect

Turn N+2:
- Ally 2 updates target
  → Scans resources: filters collected=True
  → Finds different nearest resource
  → Redirects to new target
```

**Outcome:**
- No double-collection possible
- First ally gets resource
- Second ally automatically retargets
- Efficient behavior, no wasted movement

---

## Summary

This game logic documentation covers all major systems, scenarios, and edge cases in the AI vs AI Survival Arena. The game demonstrates complex emergent behavior from relatively simple rule systems:

- **Fuzzy Logic** provides human-like decision-making
- **A* Pathfinding** ensures optimal navigation
- **Minimax Algorithm** creates challenging enemy AI
- **Dynamic Resources** keep gameplay interesting
- **Multiple Victory Conditions** create strategic depth

The interaction of these systems creates a rich tactical environment where players must balance:
- Survival (health management)
- Economy (coin collection)
- Positioning (avoiding enemies)
- Time pressure (50 turn limit)

All while competing against an equally-capable AI opponent.
