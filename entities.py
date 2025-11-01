"""
Entity classes for the game: Player, Ally, Enemy, Resource, Obstacle
"""

from constants import MAX_HEALTH, HEALTH_PACK_RESTORE, COIN_VALUE, ACTIONS


class Player:
    """AI-controlled player entity."""

    def __init__(self, position, team, color):
        """
        Initialize a player.

        Args:
            position: (x, y) starting position
            team: "Blue" or "Red"
            color: RGB color tuple
        """
        self.position = position
        self.team = team
        self.color = color
        self.health = MAX_HEALTH
        self.score = 0
        self.decision_state = ACTIONS["DEFENSIVE_PLAY"]
        self.alive = True
        self.target_position = None

    def take_damage(self, damage):
        """Apply damage to the player."""
        self.health = max(0, self.health - damage)
        if self.health <= 0:
            self.alive = False

    def heal(self, amount):
        """Heal the player."""
        self.health = min(MAX_HEALTH, self.health + amount)

    def add_score(self, points):
        """Add points to the player's score."""
        self.score += points

    def move_to(self, new_position):
        """Move the player to a new position."""
        self.position = new_position

    def __repr__(self):
        return f"Player({self.team}, HP:{self.health}, Score:{self.score})"


class Ally:
    """Ally bot that collects resources for its owner."""

    def __init__(self, position, owner, color):
        """
        Initialize an ally bot.

        Args:
            position: (x, y) starting position
            owner: Player object that owns this ally
            color: RGB color tuple
        """
        self.position = position
        self.owner = owner
        self.color = color
        self.target_resource = None

    def move_to(self, new_position):
        """Move the ally to a new position."""
        self.position = new_position

    def __repr__(self):
        return f"Ally(Owner:{self.owner.team}, Pos:{self.position})"


class Enemy:
    """Enemy agent that attacks players."""

    def __init__(self, position, color):
        """
        Initialize an enemy.

        Args:
            position: (x, y) starting position
            color: RGB color tuple
        """
        self.position = position
        self.color = color
        self.target_player = None
        self.target_position = None

    def move_to(self, new_position):
        """Move the enemy to a new position."""
        self.position = new_position

    def __repr__(self):
        return f"Enemy(Pos:{self.position})"


class Resource:
    """Resource entity (health pack or coin)."""

    def __init__(self, position, resource_type, color):
        """
        Initialize a resource.

        Args:
            position: (x, y) position
            resource_type: "health" or "coin"
            color: RGB color tuple
        """
        self.position = position
        self.type = resource_type
        self.color = color
        self.collected = False

    def collect(self, player):
        """
        Collect the resource.

        Args:
            player: Player object collecting the resource

        Returns:
            True if collected, False otherwise
        """
        if self.collected:
            return False

        if self.type == "health":
            player.heal(HEALTH_PACK_RESTORE)
        elif self.type == "coin":
            player.add_score(COIN_VALUE)

        self.collected = True
        return True

    def __repr__(self):
        return f"Resource({self.type}, Pos:{self.position})"


class Obstacle:
    """Static obstacle that blocks movement."""

    def __init__(self, position, color):
        """
        Initialize an obstacle.

        Args:
            position: (x, y) position
            color: RGB color tuple
        """
        self.position = position
        self.color = color

    def __repr__(self):
        return f"Obstacle(Pos:{self.position})"
