"""
Pygame rendering system for the AI vs AI Survival Arena
Modern UI design with custom PNG assets
"""

import pygame
import math
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    GRID_SIZE,
    CELL_SIZE,
    GRID_WIDTH,
    GRID_HEIGHT,
    GRID_OFFSET_X,
    GRID_OFFSET_Y,
    SIDEBAR_X,
    COLORS,
    MAX_HEALTH,
)
from assets import get_assets


class GameRenderer:
    """Handles all rendering for the game with modern UI."""

    def __init__(self, screen):
        """Initialize the renderer."""
        self.screen = screen
        self.debug_mode = False

        # Load all game assets (images)
        self.assets = get_assets()

        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 64)
        self.card_title_font = pygame.font.Font(None, 28)
        self.card_value_font = pygame.font.Font(None, 56)
        self.text_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.legend_font = pygame.font.Font(None, 26)

    def render_game(self, game):
        """Render the entire game state."""
        # Clear screen with background
        self.screen.fill(COLORS["background"])

        # Draw rounded border
        self._draw_border()

        # Draw title
        self._draw_title()

        # Draw stat cards
        self._draw_stat_cards(game)

        # Draw grid
        self._draw_grid_container()
        self._draw_grid(game)

        # Draw sidebar
        self._draw_sidebar(game)

        # Draw game over screen if applicable
        if not game.is_active():
            self._draw_game_over(game)

    def _draw_border(self):
        """Draw the rounded border around the screen."""
        border_rect = pygame.Rect(10, 10, WINDOW_WIDTH - 20, WINDOW_HEIGHT - 20)
        pygame.draw.rect(self.screen, COLORS["border"], border_rect, 6, border_radius=20)

    def _draw_title(self):
        """Draw the title with game controller icon."""
        # Draw gamepad icon (image)
        gamepad_icon = self.assets.get_ui_icon("gamepad")
        if gamepad_icon:
            icon_x = WINDOW_WIDTH // 2 - 150
            icon_y = 33
            self.screen.blit(gamepad_icon, (icon_x, icon_y))

        # Title text
        title_text = "Survival Arena"
        text_surface = self.title_font.render(title_text, True, COLORS["title_blue"])
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2 + 50, 50))
        self.screen.blit(text_surface, text_rect)

    def _draw_stat_cards(self, game):
        """Draw the stat cards at the top."""
        card_y = 90
        card_height = 70
        card_width = 320
        gap = 20

        # Calculate starting X to center all cards
        total_width = card_width * 4 + gap * 3
        start_x = (WINDOW_WIDTH - total_width) // 2

        # Card 1: Turn
        self._draw_card(
            start_x, card_y, card_width, card_height,
            COLORS["card_purple"], "Turn", str(game.turn_count), "clock"
        )

        # Card 2: Player 1 Health
        self._draw_card(
            start_x + card_width + gap, card_y, card_width, card_height,
            COLORS["card_purple"], f"{game.player1.team} Health",
            str(int(game.player1.health)), "heart"
        )

        # Card 3: Player 2 Health
        self._draw_card(
            start_x + (card_width + gap) * 2, card_y, card_width, card_height,
            COLORS["card_purple"], f"{game.player2.team} Health",
            str(int(game.player2.health)), "heart2"
        )

        # Card 4: Enemies
        enemy_count = len(game.enemies)
        self._draw_card(
            start_x + (card_width + gap) * 3, card_y, card_width, card_height,
            COLORS["card_red"], "Enemies", str(enemy_count), "skull"
        )

    def _draw_card(self, x, y, width, height, color, title, value, icon_type):
        """Draw a stat card with rounded corners."""
        # Card background
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, card_rect, border_radius=15)

        # Icon (left side, vertically centered) - use image
        icon_image = self.assets.get_ui_icon(icon_type)
        if icon_image:
            icon_x = x + 20
            icon_y = y + height // 2 - 10  # Center the icon vertically
            self.screen.blit(icon_image, (icon_x, icon_y))

        # Title (top, after icon)
        title_surface = self.card_title_font.render(title, True, COLORS["text_white"])
        title_rect = title_surface.get_rect(midleft=(x + 60, y + 18))
        self.screen.blit(title_surface, title_rect)

        # Value (bottom, centered)
        value_surface = self.card_value_font.render(value, True, COLORS["text_white"])
        value_rect = value_surface.get_rect(center=(x + width // 2 + 10, y + height - 20))
        self.screen.blit(value_surface, value_rect)

    def _draw_grid_container(self):
        """Draw the container for the grid."""
        container_rect = pygame.Rect(
            GRID_OFFSET_X, GRID_OFFSET_Y,
            GRID_WIDTH, GRID_HEIGHT
        )
        pygame.draw.rect(self.screen, COLORS["grid_bg"], container_rect, border_radius=15)

    def _draw_grid(self, game):
        """Draw the game grid and all entities."""
        # Draw grid lines
        for x in range(GRID_SIZE + 1):
            pixel_x = GRID_OFFSET_X + x * CELL_SIZE
            pygame.draw.line(
                self.screen, COLORS["grid_lines"],
                (pixel_x, GRID_OFFSET_Y),
                (pixel_x, GRID_OFFSET_Y + GRID_HEIGHT),
                1
            )

        for y in range(GRID_SIZE + 1):
            pixel_y = GRID_OFFSET_Y + y * CELL_SIZE
            pygame.draw.line(
                self.screen, COLORS["grid_lines"],
                (GRID_OFFSET_X, pixel_y),
                (GRID_OFFSET_X + GRID_WIDTH, pixel_y),
                1
            )

        # Draw entities
        self._draw_obstacles(game.obstacles)
        self._draw_resources(game.resources)
        self._draw_allies(game.allies)
        self._draw_enemies(game.enemies)
        self._draw_players(game.player1, game.player2)

    def _grid_to_pixel(self, grid_pos):
        """Convert grid position to pixel position (center of cell)."""
        x, y = grid_pos
        pixel_x = GRID_OFFSET_X + x * CELL_SIZE + CELL_SIZE // 2
        pixel_y = GRID_OFFSET_Y + y * CELL_SIZE + CELL_SIZE // 2
        return (pixel_x, pixel_y)

    def _draw_obstacles(self, obstacles):
        """Draw all obstacles as walls using image."""
        wall_image = self.assets.get_entity("wall")
        if not wall_image:
            return

        for obstacle in obstacles:
            x, y = self._grid_to_pixel(obstacle.position)
            # Center the image
            img_rect = wall_image.get_rect(center=(x, y))
            self.screen.blit(wall_image, img_rect)

    def _draw_resources(self, resources):
        """Draw all resources using images."""
        health_image = self.assets.get_entity("health_pack")
        coin_image = self.assets.get_entity("coin")

        for resource in resources:
            if resource.collected:
                continue

            x, y = self._grid_to_pixel(resource.position)

            if resource.type == "health" and health_image:
                img_rect = health_image.get_rect(center=(x, y))
                self.screen.blit(health_image, img_rect)

            elif resource.type == "coin" and coin_image:
                img_rect = coin_image.get_rect(center=(x, y))
                self.screen.blit(coin_image, img_rect)

    def _draw_allies(self, allies):
        """Draw all ally bots using images."""
        ally_blue_image = self.assets.get_entity("ally_blue")
        ally_red_image = self.assets.get_entity("ally_red")

        for ally in allies:
            x, y = self._grid_to_pixel(ally.position)

            # Use appropriate image based on team
            if ally.owner.team == "Blue":
                ally_image = ally_blue_image
            else:
                ally_image = ally_red_image

            if ally_image:
                img_rect = ally_image.get_rect(center=(x, y))
                self.screen.blit(ally_image, img_rect)

    def _draw_enemies(self, enemies):
        """Draw all enemies using image."""
        enemy_image = self.assets.get_entity("enemy")
        if not enemy_image:
            return

        for enemy in enemies:
            x, y = self._grid_to_pixel(enemy.position)
            img_rect = enemy_image.get_rect(center=(x, y))
            self.screen.blit(enemy_image, img_rect)

    def _draw_players(self, player1, player2):
        """Draw both players using images."""
        player_blue_image = self.assets.get_entity("player_blue")
        player_red_image = self.assets.get_entity("player_red")

        for player in [player1, player2]:
            if not player.alive:
                continue

            x, y = self._grid_to_pixel(player.position)

            # Use appropriate image based on team
            if player.team == "Blue":
                player_image = player_blue_image
            else:
                player_image = player_red_image

            if player_image:
                img_rect = player_image.get_rect(center=(x, y))
                self.screen.blit(player_image, img_rect)

    def _draw_sidebar(self, game):
        """Draw the right sidebar with info and controls."""
        sidebar_x = SIDEBAR_X

        # AI Decision Cards for both players
        y_offset = 180

        # Player 1 AI Decision
        self._draw_ai_decision_card(
            sidebar_x, y_offset, 300, 80,
            game.player1.team, game.player1.decision_state
        )

        # Player 2 AI Decision
        self._draw_ai_decision_card(
            sidebar_x + 320, y_offset, 300, 80,
            game.player2.team, game.player2.decision_state
        )

        # Score cards
        y_offset += 100
        self._draw_score_card(sidebar_x, y_offset, 300, 80, game.player1)
        self._draw_score_card(sidebar_x + 320, y_offset, 300, 80, game.player2)

        # Info text
        y_offset += 100
        self._draw_info_card(sidebar_x, y_offset, 620)

        # Restart button
        y_offset += 100
        self._draw_restart_button(sidebar_x + 200, y_offset)

        # Legend
        y_offset += 100
        self._draw_legend(sidebar_x, y_offset)

    def _draw_ai_decision_card(self, x, y, width, height, team, decision):
        """Draw AI decision card."""
        # Card background
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, COLORS["card_yellow"], card_rect, border_radius=12)

        # Brain icon (image)
        brain_icon = self.assets.get_ui_icon("brain")
        if brain_icon:
            self.screen.blit(brain_icon, (x + 20, y + 30))

        # Title
        title = f"{team} AI"
        title_surface = self.small_font.render(title, True, COLORS["text_red"])
        title_rect = title_surface.get_rect(midleft=(x + 50, y + 20))
        self.screen.blit(title_surface, title_rect)

        # Decision value
        decision_display = decision.replace("_", " ").title()
        if len(decision_display) > 18:
            decision_display = decision_display[:15] + "..."

        decision_surface = self.card_title_font.render(decision_display, True, COLORS["text_dark"])
        decision_rect = decision_surface.get_rect(center=(x + width // 2, y + 50))
        self.screen.blit(decision_surface, decision_rect)

    def _draw_score_card(self, x, y, width, height, player):
        """Draw score card for a player."""
        # Card background
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, COLORS["card_purple"], card_rect, border_radius=12)

        # Star icon (image)
        star_icon = self.assets.get_ui_icon("star")
        if star_icon:
            icon_x = x + 22
            icon_y = y + height // 2 - 9
            self.screen.blit(star_icon, (icon_x, icon_y))

        # Team name
        team_surface = self.small_font.render(f"{player.team} Score", True, COLORS["text_white"])
        team_rect = team_surface.get_rect(midleft=(x + 60, y + 25))
        self.screen.blit(team_surface, team_rect)

        # Score value
        score_surface = self.card_value_font.render(str(player.score), True, COLORS["text_white"])
        score_rect = score_surface.get_rect(center=(x + width // 2 + 20, y + height // 2 + 5))
        self.screen.blit(score_surface, score_rect)

    def _draw_info_card(self, x, y, width):
        """Draw info card."""
        height = 70
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, COLORS["card_info"], card_rect, border_radius=12)

        # Info text
        info_text = "AI vs AI Battle - Watch the algorithms compete!"
        info_surface = self.card_title_font.render(info_text, True, COLORS["text_blue"])
        info_rect = info_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(info_surface, info_rect)

    def _draw_restart_button(self, x, y):
        """Draw restart button."""
        width = 220
        height = 60
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, COLORS["card_green"], button_rect, border_radius=12)

        # Restart icon (image)
        restart_icon = self.assets.get_ui_icon("restart")
        if restart_icon:
            icon_x = x + 42
            icon_y = y + height // 2 - 9
            self.screen.blit(restart_icon, (icon_x, icon_y))

        # Text
        text = "Restart"
        text_surface = self.text_font.render(text, True, COLORS["text_white"])
        text_rect = text_surface.get_rect(center=(x + width // 2 + 20, y + height // 2))
        self.screen.blit(text_surface, text_rect)

        # Note: Press R
        note_surface = self.small_font.render("Press R", True, COLORS["text_dark"])
        note_rect = note_surface.get_rect(center=(x + width // 2, y + height + 20))
        self.screen.blit(note_surface, note_rect)

    def _draw_legend(self, x, y):
        """Draw legend showing entity types."""
        legend_items = [
            ("player1", "Blue Player", "ally1", "Blue Ally"),
            ("player2", "Red Player", "ally2", "Red Ally"),
            ("enemy", "Enemy", "health", "Health"),
            ("coin", "Coin", "wall", "Wall")
        ]

        row_height = 40
        col_width = 310

        for i, (type1, label1, type2, label2) in enumerate(legend_items):
            row_y = y + i * row_height

            # Left item icon
            self._draw_legend_icon(x, row_y + 10, type1)
            label_surface1 = self.legend_font.render(label1, True, COLORS["text_dark"])
            self.screen.blit(label_surface1, (x + 35, row_y + 5))

            # Right item icon
            self._draw_legend_icon(x + col_width, row_y + 10, type2)
            label_surface2 = self.legend_font.render(label2, True, COLORS["text_dark"])
            self.screen.blit(label_surface2, (x + col_width + 35, row_y + 5))

    def _draw_legend_icon(self, x, y, entity_type):
        """Draw a small icon for the legend using PNG images."""
        # Map entity_type to asset name
        asset_map = {
            "player1": "player_blue",
            "player2": "player_red",
            "ally1": "ally_blue",
            "ally2": "ally_red",
            "enemy": "enemy",
            "health": "health_pack",
            "coin": "coin",
            "wall": "wall"
        }

        asset_name = asset_map.get(entity_type)
        if not asset_name:
            return

        # Get the legend icon
        legend_icon = self.assets.get_legend_icon(asset_name)
        if legend_icon:
            # Center the icon at (x, y)
            icon_rect = legend_icon.get_rect(center=(x, y))
            self.screen.blit(legend_icon, icon_rect)

    def _draw_game_over(self, game):
        """Draw game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill((240, 242, 248))
        self.screen.blit(overlay, (0, 0))

        # Game Over container
        container_width = 800
        container_height = 500
        container_x = (WINDOW_WIDTH - container_width) // 2
        container_y = (WINDOW_HEIGHT - container_height) // 2

        # Container background
        container_rect = pygame.Rect(container_x, container_y, container_width, container_height)
        pygame.draw.rect(self.screen, (255, 255, 255), container_rect, border_radius=20)
        pygame.draw.rect(self.screen, COLORS["border"], container_rect, 5, border_radius=20)

        # Game Over text
        game_over_text = self.title_font.render("GAME OVER", True, COLORS["text_red"])
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, container_y + 80))
        self.screen.blit(game_over_text, game_over_rect)

        # Winner announcement
        winner_text = self.text_font.render(game.game_over_reason, True, COLORS["title_blue"])
        winner_rect = winner_text.get_rect(center=(WINDOW_WIDTH // 2, container_y + 150))
        self.screen.blit(winner_text, winner_rect)

        # Final stats
        stats = [
            f"Final Scores:",
            f"Blue Team: {game.player1.score} points, {int(game.player1.health)} HP",
            f"Red Team: {game.player2.score} points, {int(game.player2.health)} HP",
            f"Total Turns: {game.turn_count}",
        ]

        y_offset = container_y + 220
        for stat in stats:
            stat_text = self.card_title_font.render(stat, True, COLORS["text_dark"])
            stat_rect = stat_text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(stat_text, stat_rect)
            y_offset += 45

        # Instructions
        instruction = "Press R to restart or Q to quit"
        instruction_text = self.text_font.render(instruction, True, COLORS["card_green"])
        instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, container_y + 430))
        self.screen.blit(instruction_text, instruction_rect)

    def toggle_debug_mode(self):
        """Toggle debug mode on/off."""
        self.debug_mode = not self.debug_mode
