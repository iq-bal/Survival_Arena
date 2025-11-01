"""
Pygame rendering system for the AI vs AI Survival Arena
Modern UI design with cards and custom-drawn icons
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


class GameRenderer:
    """Handles all rendering for the game with modern UI."""

    def __init__(self, screen):
        """Initialize the renderer."""
        self.screen = screen
        self.debug_mode = False

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
        # Draw gamepad icon
        icon_x = WINDOW_WIDTH // 2 - 150
        icon_y = 35
        self._draw_gamepad_icon(icon_x, icon_y, 35)

        # Title text
        title_text = "Survival Arena"
        text_surface = self.title_font.render(title_text, True, COLORS["title_blue"])
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2 + 50, 50))
        self.screen.blit(text_surface, text_rect)

    def _draw_gamepad_icon(self, x, y, size):
        """Draw a simple gamepad icon."""
        # Main body
        body_rect = pygame.Rect(x, y + 10, size, size - 10)
        pygame.draw.rect(self.screen, COLORS["title_blue"], body_rect, border_radius=8)

        # D-pad (left side)
        pygame.draw.rect(self.screen, COLORS["text_white"], (x + 8, y + 18, 8, 8))

        # Buttons (right side)
        pygame.draw.circle(self.screen, COLORS["text_white"], (x + size - 10, y + 22), 4)

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

        # Icon (left side, vertically centered)
        icon_x = x + 30
        icon_y = y + height // 2
        self._draw_icon(icon_x, icon_y, 18, icon_type, COLORS["text_white"])

        # Title (top, after icon)
        title_surface = self.card_title_font.render(title, True, COLORS["text_white"])
        title_rect = title_surface.get_rect(midleft=(x + 60, y + 18))
        self.screen.blit(title_surface, title_rect)

        # Value (bottom, centered)
        value_surface = self.card_value_font.render(value, True, COLORS["text_white"])
        value_rect = value_surface.get_rect(center=(x + width // 2 + 10, y + height - 20))
        self.screen.blit(value_surface, value_rect)

    def _draw_icon(self, x, y, size, icon_type, color):
        """Draw various icon types."""
        if icon_type == "clock":
            # Clock circle
            pygame.draw.circle(self.screen, color, (x, y), size, 3)
            # Clock hands
            pygame.draw.line(self.screen, color, (x, y), (x, y - size + 5), 3)
            pygame.draw.line(self.screen, color, (x, y), (x + size - 8, y - 5), 3)

        elif icon_type == "heart":
            # Heart shape (simplified)
            points = [
                (x, y + 5),
                (x - 10, y - 5),
                (x - 10, y - 12),
                (x, y - 8),
                (x + 10, y - 12),
                (x + 10, y - 5),
            ]
            pygame.draw.polygon(self.screen, color, points)

        elif icon_type == "heart2":
            # Heart shape (variant for second player)
            points = [
                (x, y + 5),
                (x - 10, y - 5),
                (x - 10, y - 12),
                (x, y - 8),
                (x + 10, y - 12),
                (x + 10, y - 5),
            ]
            pygame.draw.polygon(self.screen, color, points)

        elif icon_type == "skull":
            # Skull (circle with eyes)
            pygame.draw.circle(self.screen, color, (x, y - 3), size - 5)
            # Eyes
            pygame.draw.circle(self.screen, COLORS["card_red"], (x - 6, y - 5), 4)
            pygame.draw.circle(self.screen, COLORS["card_red"], (x + 6, y - 5), 4)
            # Jaw
            pygame.draw.rect(self.screen, color, (x - 8, y + 5, 16, 8))

        elif icon_type == "brain":
            # Brain (wavy circle)
            pygame.draw.circle(self.screen, color, (x, y), size - 3, 3)
            # Lines inside
            pygame.draw.line(self.screen, color, (x - 8, y - 5), (x - 5, y + 5), 2)
            pygame.draw.line(self.screen, color, (x + 5, y - 5), (x + 8, y + 5), 2)

        elif icon_type == "star":
            # Star shape
            points = []
            for i in range(10):
                angle = math.pi * 2 * i / 10 - math.pi / 2
                radius = size if i % 2 == 0 else size // 2
                px = x + math.cos(angle) * radius
                py = y + math.sin(angle) * radius
                points.append((px, py))
            pygame.draw.polygon(self.screen, color, points)

        elif icon_type == "restart":
            # Circular arrow
            pygame.draw.arc(self.screen, color, (x - size, y - size, size * 2, size * 2), 0.5, 5.5, 4)
            # Arrow head
            pygame.draw.polygon(self.screen, color, [
                (x + size - 3, y - size + 5),
                (x + size + 5, y - size),
                (x + size, y - size + 10)
            ])

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
        """Draw all obstacles as walls."""
        for obstacle in obstacles:
            x, y = self._grid_to_pixel(obstacle.position)
            rect = pygame.Rect(
                x - CELL_SIZE // 2 + 2, y - CELL_SIZE // 2 + 2,
                CELL_SIZE - 4, CELL_SIZE - 4
            )
            pygame.draw.rect(self.screen, COLORS["obstacle"], rect, border_radius=5)
            # Add texture lines
            pygame.draw.line(self.screen, (80, 85, 95),
                           (x - 8, y - 8), (x + 8, y - 8), 2)
            pygame.draw.line(self.screen, (80, 85, 95),
                           (x - 8, y), (x + 8, y), 2)

    def _draw_resources(self, resources):
        """Draw all resources."""
        for resource in resources:
            if resource.collected:
                continue

            x, y = self._grid_to_pixel(resource.position)

            if resource.type == "health":
                # Green rounded square
                bg_rect = pygame.Rect(
                    x - CELL_SIZE // 2 + 3, y - CELL_SIZE // 2 + 3,
                    CELL_SIZE - 6, CELL_SIZE - 6
                )
                pygame.draw.rect(self.screen, COLORS["health"], bg_rect, border_radius=8)

                # Draw cross/plus symbol
                cross_size = 10
                pygame.draw.rect(self.screen, COLORS["text_white"],
                               (x - 2, y - cross_size, 4, cross_size * 2))
                pygame.draw.rect(self.screen, COLORS["text_white"],
                               (x - cross_size, y - 2, cross_size * 2, 4))

            elif resource.type == "coin":
                # Yellow rounded square
                bg_rect = pygame.Rect(
                    x - CELL_SIZE // 2 + 3, y - CELL_SIZE // 2 + 3,
                    CELL_SIZE - 6, CELL_SIZE - 6
                )
                pygame.draw.rect(self.screen, COLORS["coin"], bg_rect, border_radius=8)

                # Draw coin circle
                pygame.draw.circle(self.screen, (255, 200, 0), (x, y), 10)
                pygame.draw.circle(self.screen, COLORS["coin"], (x, y), 8)
                # Dollar sign
                dollar_surface = self.small_font.render("$", True, (200, 160, 0))
                dollar_rect = dollar_surface.get_rect(center=(x, y))
                self.screen.blit(dollar_surface, dollar_rect)

    def _draw_allies(self, allies):
        """Draw all ally bots."""
        for ally in allies:
            x, y = self._grid_to_pixel(ally.position)

            # Determine color based on owner
            if ally.owner.team == "Blue":
                bg_color = COLORS["ally1"]  # Blue ally
            else:
                bg_color = COLORS["ally2"]  # Red ally

            # Draw rounded square background
            bg_rect = pygame.Rect(
                x - CELL_SIZE // 2 + 3, y - CELL_SIZE // 2 + 3,
                CELL_SIZE - 6, CELL_SIZE - 6
            )
            pygame.draw.rect(self.screen, bg_color, bg_rect, border_radius=8)

            # Draw robot (simple geometric robot)
            # Head
            pygame.draw.rect(self.screen, COLORS["text_white"], (x - 6, y - 8, 12, 10), border_radius=2)
            # Eyes
            pygame.draw.circle(self.screen, bg_color, (x - 3, y - 5), 2)
            pygame.draw.circle(self.screen, bg_color, (x + 3, y - 5), 2)
            # Antenna
            pygame.draw.line(self.screen, COLORS["text_white"], (x, y - 8), (x, y - 12), 2)
            pygame.draw.circle(self.screen, COLORS["text_white"], (x, y - 12), 2)

    def _draw_enemies(self, enemies):
        """Draw all enemies."""
        for enemy in enemies:
            x, y = self._grid_to_pixel(enemy.position)

            # Draw rounded square background
            bg_rect = pygame.Rect(
                x - CELL_SIZE // 2 + 3, y - CELL_SIZE // 2 + 3,
                CELL_SIZE - 6, CELL_SIZE - 6
            )
            pygame.draw.rect(self.screen, COLORS["enemy"], bg_rect, border_radius=8)

            # Draw skull
            # Head circle
            pygame.draw.circle(self.screen, COLORS["text_white"], (x, y - 2), 10)
            # Eyes (dark circles)
            pygame.draw.circle(self.screen, COLORS["enemy"], (x - 4, y - 4), 3)
            pygame.draw.circle(self.screen, COLORS["enemy"], (x + 4, y - 4), 3)
            # Jaw
            pygame.draw.rect(self.screen, COLORS["text_white"], (x - 6, y + 5, 12, 6), border_radius=2)

    def _draw_players(self, player1, player2):
        """Draw both players."""
        for player in [player1, player2]:
            if not player.alive:
                continue

            x, y = self._grid_to_pixel(player.position)

            # Draw rounded square background
            bg_rect = pygame.Rect(
                x - CELL_SIZE // 2 + 2, y - CELL_SIZE // 2 + 2,
                CELL_SIZE - 4, CELL_SIZE - 4
            )

            # Use different colors for each player
            if player.team == "Blue":
                bg_color = COLORS["player1"]  # Blue
            else:
                bg_color = COLORS["player2"]  # Red

            pygame.draw.rect(self.screen, bg_color, bg_rect, border_radius=8)

            # Draw smiley face
            # Face circle
            pygame.draw.circle(self.screen, (255, 240, 200), (x, y), 12)
            # Eyes
            pygame.draw.circle(self.screen, (50, 50, 50), (x - 5, y - 3), 2)
            pygame.draw.circle(self.screen, (50, 50, 50), (x + 5, y - 3), 2)
            # Smile
            pygame.draw.arc(self.screen, (50, 50, 50), (x - 6, y - 2, 12, 10), 0.5, 2.6, 2)

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

        # Brain icon
        self._draw_icon(x + 30, y + 40, 18, "brain", COLORS["text_red"])

        # Title
        title = f"{team} AI"
        title_surface = self.small_font.render(title, True, COLORS["text_red"])
        title_rect = title_surface.get_rect(midleft=(x + 60, y + 20))
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

        # Star icon
        self._draw_icon(x + 30, y + height // 2, 15, "star", COLORS["text_white"])

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

        # Restart icon
        self._draw_icon(x + 50, y + height // 2, 15, "restart", COLORS["text_white"])

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
        """Draw a small icon for the legend - matches game entity appearance."""
        size = 18

        if entity_type == "player1":
            # Blue Player - Blue background with smiley (matches game)
            bg_rect = pygame.Rect(x - 8, y - 8, 16, 16)
            pygame.draw.rect(self.screen, COLORS["player1"], bg_rect, border_radius=4)
            # Smiley face
            pygame.draw.circle(self.screen, (255, 240, 200), (x, y), 6)
            pygame.draw.circle(self.screen, (50, 50, 50), (x - 3, y - 2), 1)
            pygame.draw.circle(self.screen, (50, 50, 50), (x + 3, y - 2), 1)
            pygame.draw.arc(self.screen, (50, 50, 50), (x - 3, y - 1, 6, 5), 0.5, 2.6, 1)

        elif entity_type == "player2":
            # Red Player - Red background with smiley (matches game)
            bg_rect = pygame.Rect(x - 8, y - 8, 16, 16)
            pygame.draw.rect(self.screen, COLORS["player2"], bg_rect, border_radius=4)
            # Smiley face
            pygame.draw.circle(self.screen, (255, 240, 200), (x, y), 6)
            pygame.draw.circle(self.screen, (50, 50, 50), (x - 3, y - 2), 1)
            pygame.draw.circle(self.screen, (50, 50, 50), (x + 3, y - 2), 1)
            pygame.draw.arc(self.screen, (50, 50, 50), (x - 3, y - 1, 6, 5), 0.5, 2.6, 1)

        elif entity_type == "ally1":
            # Blue Ally - Blue robot (matches game)
            bg_rect = pygame.Rect(x - 8, y - 8, 16, 16)
            pygame.draw.rect(self.screen, COLORS["ally1"], bg_rect, border_radius=4)
            # Robot details
            pygame.draw.rect(self.screen, COLORS["text_white"], (x - 3, y - 4, 6, 5), border_radius=1)
            pygame.draw.circle(self.screen, COLORS["ally1"], (x - 2, y - 2), 1)
            pygame.draw.circle(self.screen, COLORS["ally1"], (x + 2, y - 2), 1)
            pygame.draw.line(self.screen, COLORS["text_white"], (x, y - 4), (x, y - 6), 1)
            pygame.draw.circle(self.screen, COLORS["text_white"], (x, y - 6), 1)

        elif entity_type == "ally2":
            # Red Ally - Red robot (matches game)
            bg_rect = pygame.Rect(x - 8, y - 8, 16, 16)
            pygame.draw.rect(self.screen, COLORS["ally2"], bg_rect, border_radius=4)
            # Robot details
            pygame.draw.rect(self.screen, COLORS["text_white"], (x - 3, y - 4, 6, 5), border_radius=1)
            pygame.draw.circle(self.screen, COLORS["ally2"], (x - 2, y - 2), 1)
            pygame.draw.circle(self.screen, COLORS["ally2"], (x + 2, y - 2), 1)
            pygame.draw.line(self.screen, COLORS["text_white"], (x, y - 4), (x, y - 6), 1)
            pygame.draw.circle(self.screen, COLORS["text_white"], (x, y - 6), 1)

        elif entity_type == "enemy":
            # Enemy - Purple background with skull (matches game)
            bg_rect = pygame.Rect(x - 8, y - 8, 16, 16)
            pygame.draw.rect(self.screen, COLORS["enemy"], bg_rect, border_radius=4)
            # Skull
            pygame.draw.circle(self.screen, COLORS["text_white"], (x, y - 1), 5)
            pygame.draw.circle(self.screen, COLORS["enemy"], (x - 2, y - 2), 2)
            pygame.draw.circle(self.screen, COLORS["enemy"], (x + 2, y - 2), 2)
            pygame.draw.rect(self.screen, COLORS["text_white"], (x - 3, y + 3, 6, 3), border_radius=1)

        elif entity_type == "health":
            # Health - Green background with cross (matches game)
            bg_rect = pygame.Rect(x - 8, y - 8, 16, 16)
            pygame.draw.rect(self.screen, COLORS["health"], bg_rect, border_radius=4)
            # Cross
            cross_size = 5
            pygame.draw.rect(self.screen, COLORS["text_white"], (x - 1, y - cross_size, 2, cross_size * 2))
            pygame.draw.rect(self.screen, COLORS["text_white"], (x - cross_size, y - 1, cross_size * 2, 2))

        elif entity_type == "coin":
            # Coin - Yellow background with coin circle (matches game)
            bg_rect = pygame.Rect(x - 8, y - 8, 16, 16)
            pygame.draw.rect(self.screen, COLORS["coin"], bg_rect, border_radius=4)
            # Coin circle
            pygame.draw.circle(self.screen, (255, 200, 0), (x, y), 5)
            pygame.draw.circle(self.screen, COLORS["coin"], (x, y), 4)

        elif entity_type == "wall":
            # Wall - Gray square with texture (matches game)
            bg_rect = pygame.Rect(x - 8, y - 8, 16, 16)
            pygame.draw.rect(self.screen, COLORS["obstacle"], bg_rect, border_radius=3)
            # Texture lines
            pygame.draw.line(self.screen, (80, 85, 95), (x - 4, y - 4), (x + 4, y - 4), 1)
            pygame.draw.line(self.screen, (80, 85, 95), (x - 4, y), (x + 4, y), 1)

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
