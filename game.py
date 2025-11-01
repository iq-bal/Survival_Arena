"""
Main game logic for AI vs AI Survival Arena
"""

import random
from entities import Player, Ally, Enemy, Resource, Obstacle
from ai.astar import AStarPathfinder
from ai.minimax import MinimaxAI
from ai.fuzzy_logic import FuzzyLogic
from constants import (
    GRID_SIZE,
    MAX_ENEMIES,
    MAX_OBSTACLES,
    MAX_HEALTH_PACKS,
    MAX_COINS,
    RESOURCE_SPAWN_CHANCE,
    COLORS,
    ACTIONS,
    WIN_SCORE,
    MAX_TURNS,
    ENEMY_DAMAGE,
    PLAYER_COLLISION_DAMAGE,
    MINIMAX_DEPTH,
)


class SurvivalArenaGame:
    """Main game class managing all entities and game logic."""

    def __init__(self):
        """Initialize the game."""
        self.grid_size = GRID_SIZE
        self.turn_count = 0
        self.game_active = True
        self.winner = None
        self.game_over_reason = ""

        # Initialize entities
        self.player1 = None
        self.player2 = None
        self.allies = []
        self.enemies = []
        self.resources = []
        self.obstacles = []

        # Initialize game
        self.setup_game()

    def setup_game(self):
        """Set up the game with initial entities."""
        # Clear all entities
        self.allies = []
        self.enemies = []
        self.resources = []
        self.obstacles = []

        # Create obstacles first
        obstacle_positions = self._generate_random_positions(MAX_OBSTACLES, set())
        for pos in obstacle_positions:
            self.obstacles.append(Obstacle(pos, COLORS["obstacle"]))

        # Get obstacle positions for pathfinding
        obstacle_set = {obs.position for obs in self.obstacles}

        # Create players in opposite corners
        player1_pos = self._find_free_position((2, 2), obstacle_set, set())
        player2_pos = self._find_free_position(
            (GRID_SIZE - 3, GRID_SIZE - 3), obstacle_set, {player1_pos}
        )

        self.player1 = Player(player1_pos, "Blue", COLORS["player1"])
        self.player2 = Player(player2_pos, "Red", COLORS["player2"])

        # Create allies for each player
        occupied = obstacle_set | {player1_pos, player2_pos}

        # Player 1 allies (near player 1)
        ally1_pos = self._find_free_position((1, 2), obstacle_set, occupied)
        occupied.add(ally1_pos)
        ally2_pos = self._find_free_position((2, 1), obstacle_set, occupied)
        occupied.add(ally2_pos)

        self.allies.append(Ally(ally1_pos, self.player1, COLORS["ally1"]))
        self.allies.append(Ally(ally2_pos, self.player1, COLORS["ally1"]))

        # Player 2 allies (near player 2)
        ally3_pos = self._find_free_position(
            (GRID_SIZE - 2, GRID_SIZE - 3), obstacle_set, occupied
        )
        occupied.add(ally3_pos)
        ally4_pos = self._find_free_position(
            (GRID_SIZE - 3, GRID_SIZE - 2), obstacle_set, occupied
        )
        occupied.add(ally4_pos)

        self.allies.append(Ally(ally3_pos, self.player2, COLORS["ally2"]))
        self.allies.append(Ally(ally4_pos, self.player2, COLORS["ally2"]))

        # Create enemies
        for i in range(MAX_ENEMIES):
            enemy_pos = self._find_free_position(
                (GRID_SIZE // 2, GRID_SIZE // 2), obstacle_set, occupied
            )
            occupied.add(enemy_pos)
            self.enemies.append(Enemy(enemy_pos, COLORS["enemy"]))

        # Spawn initial resources
        self._spawn_resources()

    def _generate_random_positions(self, count, forbidden):
        """Generate random unique positions avoiding forbidden positions."""
        positions = set()
        attempts = 0
        max_attempts = count * 10

        while len(positions) < count and attempts < max_attempts:
            pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if pos not in forbidden and pos not in positions:
                positions.add(pos)
            attempts += 1

        return list(positions)

    def _find_free_position(self, preferred, obstacles, occupied):
        """Find a free position near the preferred location."""
        # Try preferred position first
        if preferred not in obstacles and preferred not in occupied:
            return preferred

        # Try nearby positions
        for radius in range(1, 5):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    pos = (preferred[0] + dx, preferred[1] + dy)
                    if (
                        0 <= pos[0] < GRID_SIZE
                        and 0 <= pos[1] < GRID_SIZE
                        and pos not in obstacles
                        and pos not in occupied
                    ):
                        return pos

        # Fallback: find any free position
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                pos = (x, y)
                if pos not in obstacles and pos not in occupied:
                    return pos

        return preferred  # Last resort

    def _spawn_resources(self):
        """Spawn initial resources."""
        obstacle_positions = {obs.position for obs in self.obstacles}
        occupied = obstacle_positions | {self.player1.position, self.player2.position}
        occupied |= {ally.position for ally in self.allies}
        occupied |= {enemy.position for enemy in self.enemies}

        # Spawn health packs
        health_count = len([r for r in self.resources if r.type == "health" and not r.collected])
        for _ in range(MAX_HEALTH_PACKS - health_count):
            pos = self._find_free_position(
                (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)),
                obstacle_positions,
                occupied,
            )
            occupied.add(pos)
            self.resources.append(Resource(pos, "health", COLORS["health"]))

        # Spawn coins
        coin_count = len([r for r in self.resources if r.type == "coin" and not r.collected])
        for _ in range(MAX_COINS - coin_count):
            pos = self._find_free_position(
                (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)),
                obstacle_positions,
                occupied,
            )
            occupied.add(pos)
            self.resources.append(Resource(pos, "coin", COLORS["coin"]))

    def _try_spawn_new_resources(self):
        """Randomly spawn new resources during gameplay."""
        if random.random() < RESOURCE_SPAWN_CHANCE:
            obstacle_positions = {obs.position for obs in self.obstacles}
            occupied = obstacle_positions | {self.player1.position, self.player2.position}
            occupied |= {ally.position for ally in self.allies}
            occupied |= {enemy.position for enemy in self.enemies}
            occupied |= {r.position for r in self.resources if not r.collected}

            # Try to spawn a health pack
            health_count = len([r for r in self.resources if r.type == "health" and not r.collected])
            if health_count < MAX_HEALTH_PACKS:
                pos = self._find_free_position(
                    (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)),
                    obstacle_positions,
                    occupied,
                )
                self.resources.append(Resource(pos, "health", COLORS["health"]))

        if random.random() < RESOURCE_SPAWN_CHANCE:
            obstacle_positions = {obs.position for obs in self.obstacles}
            occupied = obstacle_positions | {self.player1.position, self.player2.position}
            occupied |= {ally.position for ally in self.allies}
            occupied |= {enemy.position for enemy in self.enemies}
            occupied |= {r.position for r in self.resources if not r.collected}

            # Try to spawn a coin
            coin_count = len([r for r in self.resources if r.type == "coin" and not r.collected])
            if coin_count < MAX_COINS:
                pos = self._find_free_position(
                    (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)),
                    obstacle_positions,
                    occupied,
                )
                self.resources.append(Resource(pos, "coin", COLORS["coin"]))

    def execute_turn(self):
        """Execute one turn of the game."""
        if not self.game_active:
            return

        # Get obstacle positions
        obstacle_positions = {obs.position for obs in self.obstacles}

        # 1. Player 1 AI Decision and Movement
        self._update_player(self.player1, obstacle_positions)

        # 2. Player 2 AI Decision and Movement
        self._update_player(self.player2, obstacle_positions)

        # 3. Update all Allies
        self._update_allies(obstacle_positions)

        # 4. Update all Enemies
        self._update_enemies(obstacle_positions)

        # 5. Check collisions
        self._check_collisions()

        # 6. Spawn new resources
        self._try_spawn_new_resources()

        # 7. Increment turn counter
        self.turn_count += 1

        # 8. Check game over conditions
        self.check_game_over()

    def _update_player(self, player, obstacles):
        """Update player AI decision and movement."""
        if not player.alive:
            return

        # Get game state for fuzzy logic
        nearest_enemy_dist = self._get_nearest_enemy_distance(player.position)
        nearest_resource_dist = self._get_nearest_resource_distance(player.position)

        # Make decision using fuzzy logic
        action = FuzzyLogic.decide_action(
            player.health, player.score, nearest_enemy_dist, nearest_resource_dist
        )
        player.decision_state = action

        # Determine target based on action
        target = None

        if action == ACTIONS["FLEE_ENEMY"]:
            # Move away from nearest enemy
            target = self._get_flee_position(player.position, obstacles)
        elif action == ACTIONS["SEEK_HEALTH"]:
            # Move toward nearest health pack
            target = self._get_nearest_resource_position(player.position, "health")
        elif action == ACTIONS["COLLECT_COINS"]:
            # Move toward nearest coin
            target = self._get_nearest_resource_position(player.position, "coin")
        elif action == ACTIONS["COLLECT_RESOURCES"]:
            # Move toward nearest resource
            target = self._get_nearest_resource_position(player.position, None)
        elif action == ACTIONS["AGGRESSIVE_PLAY"]:
            # Move toward opponent
            opponent = self.player2 if player == self.player1 else self.player1
            target = opponent.position
        elif action == ACTIONS["DEFENSIVE_PLAY"]:
            # Balanced: move toward resources while avoiding enemies
            target = self._get_nearest_resource_position(player.position, None)

        # Move toward target using A*
        if target:
            player.target_position = target
            next_pos = AStarPathfinder.get_next_move(
                player.position, target, obstacles, GRID_SIZE
            )
            player.move_to(next_pos)

    def _update_allies(self, obstacles):
        """Update all ally bots using A* pathfinding."""
        for ally in self.allies:
            # Find nearest unclaimed resource
            nearest_resource = None
            min_distance = float("inf")

            for resource in self.resources:
                if not resource.collected:
                    dist = AStarPathfinder.manhattan_distance(ally.position, resource.position)
                    if dist < min_distance:
                        min_distance = dist
                        nearest_resource = resource

            if nearest_resource:
                ally.target_resource = nearest_resource
                # Move toward resource using A*
                next_pos = AStarPathfinder.get_next_move(
                    ally.position, nearest_resource.position, obstacles, GRID_SIZE
                )
                ally.move_to(next_pos)

    def _update_enemies(self, obstacles):
        """Update all enemies using Minimax algorithm."""
        for enemy in self.enemies:
            # Use Minimax to choose target and move
            if self.player1.alive and self.player2.alive:
                target, next_move = MinimaxAI.choose_target_and_move(
                    enemy.position,
                    self.player1.position,
                    self.player2.position,
                    self.player1.health,
                    self.player2.health,
                    obstacles,
                    GRID_SIZE,
                    MINIMAX_DEPTH,
                )
                enemy.target_position = target
                enemy.move_to(next_move)
            elif self.player1.alive:
                # Only player 1 alive, chase them
                enemy.target_position = self.player1.position
                next_move = AStarPathfinder.get_next_move(
                    enemy.position, self.player1.position, obstacles, GRID_SIZE
                )
                enemy.move_to(next_move)
            elif self.player2.alive:
                # Only player 2 alive, chase them
                enemy.target_position = self.player2.position
                next_move = AStarPathfinder.get_next_move(
                    enemy.position, self.player2.position, obstacles, GRID_SIZE
                )
                enemy.move_to(next_move)

    def _check_collisions(self):
        """Check and handle all collisions."""
        # Player-Enemy collisions
        for enemy in self.enemies:
            if self.player1.alive and enemy.position == self.player1.position:
                self.player1.take_damage(ENEMY_DAMAGE)
            if self.player2.alive and enemy.position == self.player2.position:
                self.player2.take_damage(ENEMY_DAMAGE)

        # Player-Resource collisions
        for resource in self.resources:
            if not resource.collected:
                if self.player1.alive and resource.position == self.player1.position:
                    resource.collect(self.player1)
                elif self.player2.alive and resource.position == self.player2.position:
                    resource.collect(self.player2)

        # Ally-Resource collisions
        for ally in self.allies:
            for resource in self.resources:
                if not resource.collected and ally.position == resource.position:
                    resource.collect(ally.owner)

        # Player-Player collision
        if (
            self.player1.alive
            and self.player2.alive
            and self.player1.position == self.player2.position
        ):
            self.player1.take_damage(PLAYER_COLLISION_DAMAGE)
            self.player2.take_damage(PLAYER_COLLISION_DAMAGE)

    def _get_nearest_enemy_distance(self, position):
        """Get distance to nearest enemy."""
        min_dist = float("inf")
        for enemy in self.enemies:
            dist = AStarPathfinder.manhattan_distance(position, enemy.position)
            min_dist = min(min_dist, dist)
        return min_dist if min_dist != float("inf") else 20

    def _get_nearest_resource_distance(self, position):
        """Get distance to nearest resource."""
        min_dist = float("inf")
        for resource in self.resources:
            if not resource.collected:
                dist = AStarPathfinder.manhattan_distance(position, resource.position)
                min_dist = min(min_dist, dist)
        return min_dist if min_dist != float("inf") else 20

    def _get_nearest_resource_position(self, position, resource_type=None):
        """Get position of nearest resource of given type."""
        nearest = None
        min_dist = float("inf")

        for resource in self.resources:
            if not resource.collected:
                if resource_type is None or resource.type == resource_type:
                    dist = AStarPathfinder.manhattan_distance(position, resource.position)
                    if dist < min_dist:
                        min_dist = dist
                        nearest = resource.position

        return nearest if nearest else position

    def _get_flee_position(self, position, obstacles):
        """Get a position away from enemies."""
        # Find nearest enemy
        nearest_enemy = None
        min_dist = float("inf")

        for enemy in self.enemies:
            dist = AStarPathfinder.manhattan_distance(position, enemy.position)
            if dist < min_dist:
                min_dist = dist
                nearest_enemy = enemy

        if nearest_enemy:
            # Move in opposite direction
            dx = position[0] - nearest_enemy.position[0]
            dy = position[1] - nearest_enemy.position[1]

            # Normalize and scale
            if abs(dx) > abs(dy):
                dx = 1 if dx > 0 else -1
                dy = 0
            else:
                dx = 0
                dy = 1 if dy > 0 else -1

            flee_pos = (
                max(0, min(GRID_SIZE - 1, position[0] + dx * 3)),
                max(0, min(GRID_SIZE - 1, position[1] + dy * 3)),
            )

            return flee_pos

        return position

    def check_game_over(self):
        """Check if game over conditions are met."""
        # Check if a player reached win score
        if self.player1.score >= WIN_SCORE:
            self.game_active = False
            self.winner = self.player1
            self.game_over_reason = f"{self.player1.team} Team wins by score!"
            return

        if self.player2.score >= WIN_SCORE:
            self.game_active = False
            self.winner = self.player2
            self.game_over_reason = f"{self.player2.team} Team wins by score!"
            return

        # Check if a player died
        if not self.player1.alive and self.player2.alive:
            self.game_active = False
            self.winner = self.player2
            self.game_over_reason = f"{self.player2.team} Team wins by survival!"
            return

        if not self.player2.alive and self.player1.alive:
            self.game_active = False
            self.winner = self.player1
            self.game_over_reason = f"{self.player1.team} Team wins by survival!"
            return

        # Check if both players died
        if not self.player1.alive and not self.player2.alive:
            self.game_active = False
            self.winner = None
            self.game_over_reason = "Draw! Both players eliminated!"
            return

        # Check if max turns reached
        if self.turn_count >= MAX_TURNS:
            self.game_active = False
            if self.player1.score > self.player2.score:
                self.winner = self.player1
                self.game_over_reason = (
                    f"{self.player1.team} Team wins by score after {MAX_TURNS} turns!"
                )
            elif self.player2.score > self.player1.score:
                self.winner = self.player2
                self.game_over_reason = (
                    f"{self.player2.team} Team wins by score after {MAX_TURNS} turns!"
                )
            else:
                self.winner = None
                self.game_over_reason = f"Draw after {MAX_TURNS} turns!"
            return

    def is_active(self):
        """Check if game is still active."""
        return self.game_active

    def reset(self):
        """Reset the game to initial state."""
        self.turn_count = 0
        self.game_active = True
        self.winner = None
        self.game_over_reason = ""
        self.setup_game()
