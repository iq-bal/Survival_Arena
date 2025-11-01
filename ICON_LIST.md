# Icon/Image List for AI vs AI Survival Arena

## All Icons/Characters/Images Currently Used

### 1. Game Entities (In-Game Grid)

#### Players
- **Blue Player** (player1)
  - Current: Blue rounded square with yellow smiley face
  - Location: Game grid
  - Size: ~30×30 pixels
  - Features: Face with 2 eyes and smile arc

- **Red Player** (player2)
  - Current: Red rounded square with yellow smiley face
  - Location: Game grid
  - Size: ~30×30 pixels
  - Features: Face with 2 eyes and smile arc

#### Allies
- **Blue Team Ally** (ally1)
  - Current: Light blue rounded square with white robot icon
  - Location: Game grid
  - Size: ~28×28 pixels
  - Features: Robot head with eyes and antenna

- **Red Team Ally** (ally2)
  - Current: Light red rounded square with white robot icon
  - Location: Game grid
  - Size: ~28×28 pixels
  - Features: Robot head with eyes and antenna

#### Enemies
- **Enemy** (enemy)
  - Current: Purple rounded square with white skull icon
  - Location: Game grid
  - Size: ~28×28 pixels
  - Features: Skull with eye sockets and jaw

#### Resources
- **Health Pack** (health)
  - Current: Green rounded square with white cross/plus symbol
  - Location: Game grid
  - Size: ~28×28 pixels
  - Features: Medical cross symbol

- **Coin** (coin)
  - Current: Yellow rounded square with concentric circles and $ symbol
  - Location: Game grid
  - Size: ~28×28 pixels
  - Features: Coin with dollar sign

#### Obstacles
- **Wall** (wall/obstacle)
  - Current: Dark gray rounded square with texture lines
  - Location: Game grid
  - Size: ~30×30 pixels
  - Features: Horizontal texture lines

---

### 2. UI Icons (Top Stat Cards)

#### Card Icons
- **Clock Icon** (for Turn counter)
  - Current: Circle with clock hands
  - Location: Top stat card
  - Size: ~18×18 pixels
  - Purpose: Indicates turn/time

- **Heart Icon** (for Player Health - 2 variations)
  - Current: Heart shape
  - Location: Top stat cards (Blue Health, Red Health)
  - Size: ~18×18 pixels
  - Purpose: Indicates health status

- **Skull Icon** (for Enemy count)
  - Current: Skull with eyes and jaw
  - Location: Top stat card (Enemies)
  - Size: ~18×18 pixels
  - Purpose: Indicates enemy count

---

### 3. Sidebar Icons

#### Title Icon
- **Gamepad Icon** (title decoration)
  - Current: Simple gamepad shape with D-pad and buttons
  - Location: Next to "Survival Arena" title
  - Size: ~35×35 pixels
  - Purpose: Game decoration

#### AI Decision Cards
- **Brain Icon** (for AI decisions)
  - Current: Circle with wavy lines
  - Location: AI decision cards (2 cards for Blue/Red AI)
  - Size: ~18×18 pixels
  - Purpose: Indicates AI thinking/decision-making

#### Score Cards
- **Star Icon** (for Scores)
  - Current: 10-point star shape
  - Location: Score cards (Blue Score, Red Score)
  - Size: ~15×15 pixels
  - Purpose: Indicates points/score

#### Restart Button
- **Restart Icon** (circular arrow)
  - Current: Circular arc with arrow head
  - Location: Restart button
  - Size: ~15×15 pixels
  - Purpose: Indicates restart action

#### Legend Icons
All entity icons appear again in smaller form (16×16 pixels) in the legend:
- Blue Player (with smiley)
- Red Player (with smiley)
- Blue Ally (robot)
- Red Ally (robot)
- Enemy (skull)
- Health Pack (cross)
- Coin (circle with $)
- Wall (textured square)

---

## Icon Categories Summary

### Total Unique Icons: 17

1. **Players**: 2 (Blue Player, Red Player)
2. **Allies**: 2 (Blue Ally, Red Ally)
3. **Enemy**: 1
4. **Resources**: 2 (Health Pack, Coin)
5. **Obstacle**: 1 (Wall)
6. **UI Icons**: 9 (Clock, Heart ×2, Skull, Gamepad, Brain, Star, Restart)

---

## Recommended Image Sizes for Replacements

### Game Grid Entities
- **Players**: 32×32 pixels PNG with transparency
- **Allies**: 28×28 pixels PNG with transparency
- **Enemies**: 28×28 pixels PNG with transparency
- **Resources**: 28×28 pixels PNG with transparency
- **Obstacles**: 30×30 pixels PNG (can be opaque)

### UI Icons
- **Stat Card Icons**: 20×20 pixels PNG with transparency
- **Sidebar Icons**: 18×18 pixels PNG with transparency
- **Title Gamepad**: 40×40 pixels PNG with transparency
- **Legend Icons**: 16×16 pixels PNG with transparency

---

## File Naming Convention (Suggested)

```
icons/
├── entities/
│   ├── player_blue.png          # Blue player
│   ├── player_red.png            # Red player
│   ├── ally_blue.png             # Blue ally
│   ├── ally_red.png              # Red ally
│   ├── enemy.png                 # Enemy
│   ├── health_pack.png           # Health resource
│   ├── coin.png                  # Coin resource
│   └── wall.png                  # Obstacle
│
├── ui/
│   ├── icon_clock.png            # Turn counter
│   ├── icon_heart.png            # Health indicator
│   ├── icon_skull.png            # Enemy count
│   ├── icon_gamepad.png          # Title decoration
│   ├── icon_brain.png            # AI decision
│   ├── icon_star.png             # Score
│   └── icon_restart.png          # Restart button
│
└── legend/
    ├── legend_player_blue.png    # 16×16 version
    ├── legend_player_red.png     # 16×16 version
    ├── legend_ally_blue.png      # 16×16 version
    ├── legend_ally_red.png       # 16×16 version
    ├── legend_enemy.png          # 16×16 version
    ├── legend_health.png         # 16×16 version
    ├── legend_coin.png           # 16×16 version
    └── legend_wall.png           # 16×16 version
```

---

## Notes

1. All images should have **transparent backgrounds** except obstacles/walls
2. Use **PNG format** for best quality with transparency
3. Images should be **square** (same width and height)
4. Consider providing **2× versions** for high-DPI displays (optional)
5. **Color scheme**: Blue team = blue tones, Red team = red tones, Enemies = purple, Health = green, Coins = gold

---

## Implementation

Once you provide the custom images, they can be loaded using:
```python
# In rendering.py or a new assets.py file
icon_player_blue = pygame.image.load('icons/entities/player_blue.png')
icon_player_red = pygame.image.load('icons/entities/player_red.png')
# ... etc
```

And drawn with:
```python
self.screen.blit(icon_player_blue, (x, y))
```
