"""
Pygame rendering system for the AI vs AI Survival Arena
"""

import pygame
import math
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    GRID_SIZE,
    CELL_SIZE,
    COLORS,
    MAX_HEALTH,
)


class GameRenderer:
    """Handles all rendering for the game."""

    def __init__(self, screen):
        """
        Initialize the renderer.

        Args:
            screen: Pygame screen surface
        """
        self.screen = screen
        self.font = None
        self.title_font = None
        self.debug_mode = False

        # Initialize fonts
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 18)

    def render_game(self, game):
        """
        Render the entire game state.

        Args:
            game: SurvivalArenaGame instance
        """
        # Clear screen
        self.screen.fill(COLORS["background"])

        # Draw grid
        self._draw_grid()

        # Draw entities
        self._draw_obstacles(game.obstacles)
        self._draw_resources(game.resources)
        self._draw_allies(game.allies)
        self._draw_enemies(game.enemies)
        self._draw_players(game.player1, game.player2)

        # Draw UI
        self._draw_ui(game)

        # Draw game over screen if applicable
        if not game.is_active():
            self._draw_game_over(game)

    def _draw_grid(self):
        """Draw the grid lines."""
        for x in range(0, WINDOW_WIDTH + 1, CELL_SIZE):
            pygame.draw.line(
                self.screen, COLORS["grid_lines"], (x, 0), (x, WINDOW_HEIGHT), 1
            )

        for y in range(0, WINDOW_HEIGHT + 1, CELL_SIZE):
            pygame.draw.line(
                self.screen, COLORS["grid_lines"], (0, y), (WINDOW_WIDTH, y), 1
            )

    def _grid_to_pixel(self, grid_pos):
        """Convert grid position to pixel position (center of cell)."""
        x, y = grid_pos
        pixel_x = x * CELL_SIZE + CELL_SIZE // 2
        pixel_y = y * CELL_SIZE + CELL_SIZE // 2
        return (pixel_x, pixel_y)

    def _draw_obstacles(self, obstacles):
        """Draw all obstacles."""
        for obstacle in obstacles:
            x, y = self._grid_to_pixel(obstacle.position)
            rect = pygame.Rect(
                x - CELL_SIZE // 2, y - CELL_SIZE // 2, CELL_SIZE, CELL_SIZE
            )
            pygame.draw.rect(self.screen, obstacle.color, rect)

    def _draw_resources(self, resources):
        """Draw all resources."""
        for resource in resources:
            if resource.collected:
                continue

            x, y = self._grid_to_pixel(resource.position)

            if resource.type == "health":
                # Draw green cross (health pack)
                pygame.draw.circle(self.screen, resource.color, (x, y), CELL_SIZE // 3)
                # Draw cross
                cross_size = CELL_SIZE // 4
                pygame.draw.rect(
                    self.screen,
                    (255, 255, 255),
                    (x - 2, y - cross_size, 4, cross_size * 2),
                )
                pygame.draw.rect(
                    self.screen,
                    (255, 255, 255),
                    (x - cross_size, y - 2, cross_size * 2, 4),
                )
            elif resource.type == "coin":
                # Draw gold coin
                pygame.draw.circle(self.screen, resource.color, (x, y), CELL_SIZE // 3)
                # Draw dollar sign
                text = self.small_font.render("$", True, (0, 0, 0))
                text_rect = text.get_rect(center=(x, y))
                self.screen.blit(text, text_rect)

    def _draw_allies(self, allies):
        """Draw all ally bots."""
        for ally in allies:
            x, y = self._grid_to_pixel(ally.position)
            # Draw small circle
            pygame.draw.circle(self.screen, ally.color, (x, y), CELL_SIZE // 4)
            # Draw outline
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), CELL_SIZE // 4, 2)

    def _draw_enemies(self, enemies):
        """Draw all enemies as triangles pointing toward their target."""
        for enemy in enemies:
            x, y = self._grid_to_pixel(enemy.position)

            # Determine direction to point triangle
            angle = 0
            if enemy.target_position:
                dx = enemy.target_position[0] - enemy.position[0]
                dy = enemy.target_position[1] - enemy.position[1]
                angle = math.atan2(dy, dx)

            # Calculate triangle points
            size = CELL_SIZE // 3
            point1 = (x + size * math.cos(angle), y + size * math.sin(angle))
            point2 = (
                x + size * math.cos(angle + 2.5),
                y + size * math.sin(angle + 2.5),
            )
            point3 = (
                x + size * math.cos(angle - 2.5),
                y + size * math.sin(angle - 2.5),
            )

            pygame.draw.polygon(self.screen, enemy.color, [point1, point2, point3])
            # Draw outline
            pygame.draw.polygon(
                self.screen, (255, 255, 255), [point1, point2, point3], 2
            )

    def _draw_players(self, player1, player2):
        """Draw both players."""
        for player in [player1, player2]:
            if not player.alive:
                continue

            x, y = self._grid_to_pixel(player.position)

            # Draw large circle
            pygame.draw.circle(self.screen, player.color, (x, y), CELL_SIZE // 2 - 2)
            # Draw outline
            pygame.draw.circle(
                self.screen, (255, 255, 255), (x, y), CELL_SIZE // 2 - 2, 3
            )

            # Draw health bar above player
            self._draw_health_bar(
                x - CELL_SIZE // 2, y - CELL_SIZE // 2 - 10, CELL_SIZE, player.health
            )

    def _draw_health_bar(self, x, y, width, health):
        """Draw a health bar."""
        health_ratio = max(0, min(1, health / MAX_HEALTH))

        # Background
        pygame.draw.rect(self.screen, COLORS["health_bar_bg"], (x, y, width, 6))

        # Health
        health_width = int(width * health_ratio)
        if health_ratio > 0.5:
            color = COLORS["health_bar"]
        elif health_ratio > 0.25:
            color = (255, 215, 0)  # Yellow
        else:
            color = (255, 50, 50)  # Red

        pygame.draw.rect(self.screen, color, (x, y, health_width, 6))

        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, width, 6), 1)

    def _draw_ui(self, game):
        """Draw UI elements (title, stats, etc.)."""
        # Title
        title_text = self.title_font.render("AI vs AI Survival Arena", True, COLORS["text"])
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 30))

        # Draw semi-transparent background for title
        bg_rect = pygame.Rect(
            title_rect.left - 10, title_rect.top - 5, title_rect.width + 20, title_rect.height + 10
        )
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
        bg_surface.set_alpha(180)
        bg_surface.fill(COLORS["ui_panel"])
        self.screen.blit(bg_surface, bg_rect.topleft)

        self.screen.blit(title_text, title_rect)

        # Player 1 stats (left side)
        self._draw_player_stats(game.player1, 10, 80, "left")

        # Player 2 stats (right side)
        self._draw_player_stats(game.player2, WINDOW_WIDTH - 210, 80, "right")

        # Turn counter and controls (bottom)
        self._draw_bottom_ui(game)

    def _draw_player_stats(self, player, x, y, alignment):
        """Draw player statistics panel."""
        # Background panel
        panel_width = 200
        panel_height = 140
        bg_surface = pygame.Surface((panel_width, panel_height))
        bg_surface.set_alpha(200)
        bg_surface.fill(COLORS["ui_panel"])
        self.screen.blit(bg_surface, (x, y))

        # Border
        pygame.draw.rect(
            self.screen, player.color, (x, y, panel_width, panel_height), 3
        )

        # Team name
        team_text = self.font.render(f"{player.team} Team", True, player.color)
        self.screen.blit(team_text, (x + 10, y + 10))

        # Health
        health_text = self.font.render(f"Health: {int(player.health)}", True, COLORS["text"])
        self.screen.blit(health_text, (x + 10, y + 40))

        # Health bar
        self._draw_health_bar(x + 10, y + 65, panel_width - 20, player.health)

        # Score
        score_text = self.font.render(f"Score: {player.score}", True, COLORS["text"])
        self.screen.blit(score_text, (x + 10, y + 80))

        # Current action
        action_display = player.decision_state.replace("_", " ").title()
        action_text = self.small_font.render(f"Action: {action_display}", True, COLORS["text"])
        self.screen.blit(action_text, (x + 10, y + 110))

        # Status
        status = "ALIVE" if player.alive else "DEAD"
        status_color = (50, 255, 50) if player.alive else (255, 50, 50)
        status_text = self.small_font.render(status, True, status_color)
        self.screen.blit(status_text, (x + panel_width - 60, y + 10))

    def _draw_bottom_ui(self, game):
        """Draw bottom UI panel with turn counter and controls."""
        panel_height = 80
        panel_y = WINDOW_HEIGHT - panel_height

        # Background
        bg_surface = pygame.Surface((WINDOW_WIDTH, panel_height))
        bg_surface.set_alpha(200)
        bg_surface.fill(COLORS["ui_panel"])
        self.screen.blit(bg_surface, (0, panel_y))

        # Turn counter
        turn_text = self.font.render(f"Turn: {game.turn_count} / {game.turn_count}", True, COLORS["text"])
        turn_rect = turn_text.get_rect(center=(WINDOW_WIDTH // 2, panel_y + 20))
        self.screen.blit(turn_text, turn_rect)

        # Controls
        controls = [
            "SPACE: Pause/Resume",
            "R: Restart",
            "Q/ESC: Quit",
            "UP/DOWN: Speed",
        ]

        control_y = panel_y + 45
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, COLORS["text"])
            control_x = 20 + i * 180
            self.screen.blit(control_text, (control_x, control_y))

    def _draw_game_over(self, game):
        """Draw game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Game Over text
        game_over_text = self.title_font.render("GAME OVER", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100)
        )
        self.screen.blit(game_over_text, game_over_rect)

        # Winner announcement
        winner_text = self.title_font.render(game.game_over_reason, True, (255, 255, 0))
        winner_rect = winner_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)
        )
        self.screen.blit(winner_text, winner_rect)

        # Final stats
        stats = [
            f"Final Scores:",
            f"Blue Team: {game.player1.score} points, {int(game.player1.health)} HP",
            f"Red Team: {game.player2.score} points, {int(game.player2.health)} HP",
            f"Total Turns: {game.turn_count}",
            "",
            "Press R to restart or Q to quit",
        ]

        y_offset = WINDOW_HEIGHT // 2 + 40
        for stat in stats:
            stat_text = self.font.render(stat, True, (255, 255, 255))
            stat_rect = stat_text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(stat_text, stat_rect)
            y_offset += 35

    def toggle_debug_mode(self):
        """Toggle debug mode on/off."""
        self.debug_mode = not self.debug_mode
