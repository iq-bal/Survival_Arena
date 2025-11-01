#!/usr/bin/env python3
"""
AI vs AI Survival Arena - Main Entry Point

A Pygame-based simulation showcasing three advanced AI algorithms:
1. A* Pathfinding - for ally resource collection
2. Minimax with Alpha-Beta Pruning - for enemy targeting
3. Fuzzy Logic - for player strategic decisions

Two AI players compete autonomously in a survival arena.
"""

import pygame
import sys
from game import SurvivalArenaGame
from rendering import GameRenderer
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS


def main():
    """Main game loop."""
    # Initialize Pygame
    pygame.init()

    # Set up display
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("AI vs AI Survival Arena")

    # Create game and renderer
    game = SurvivalArenaGame()
    renderer = GameRenderer(screen)

    # Game loop variables
    clock = pygame.time.Clock()
    running = True
    paused = False
    current_fps = FPS

    print("=" * 60)
    print("AI vs AI Survival Arena - Game Started")
    print("=" * 60)
    print("\nControls:")
    print("  SPACE     - Pause/Resume")
    print("  R         - Restart game")
    print("  Q/ESC     - Quit")
    print("  UP/DOWN   - Increase/Decrease game speed")
    print("  D         - Toggle debug mode")
    print("\nAI Algorithms in Action:")
    print("  • A* Pathfinding - Ally bots navigate to resources")
    print("  • Minimax - Enemies choose optimal targets")
    print("  • Fuzzy Logic - Players make strategic decisions")
    print("\nWatch the AIs compete autonomously!")
    print("=" * 60)
    print()

    # Main game loop
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Pause/Resume
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    status = "PAUSED" if paused else "RESUMED"
                    print(f"\n>>> Game {status} <<<\n")

                # Restart
                elif event.key == pygame.K_r:
                    print("\n>>> Game RESTARTED <<<\n")
                    game.reset()
                    paused = False

                # Quit
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

                # Speed controls
                elif event.key == pygame.K_UP:
                    current_fps = min(60, current_fps + 5)
                    print(f"Speed increased: {current_fps} FPS")

                elif event.key == pygame.K_DOWN:
                    current_fps = max(5, current_fps - 5)
                    print(f"Speed decreased: {current_fps} FPS")

                # Debug mode
                elif event.key == pygame.K_d:
                    renderer.toggle_debug_mode()
                    status = "ON" if renderer.debug_mode else "OFF"
                    print(f"Debug mode: {status}")

        # Update game state
        if not paused and game.is_active():
            game.execute_turn()

            # Print turn info periodically
            if game.turn_count % 10 == 0:
                print(f"Turn {game.turn_count}:")
                print(
                    f"  Blue: HP={int(game.player1.health)}, "
                    f"Score={game.player1.score}, "
                    f"Action={game.player1.decision_state}"
                )
                print(
                    f"  Red:  HP={int(game.player2.health)}, "
                    f"Score={game.player2.score}, "
                    f"Action={game.player2.decision_state}"
                )
                print()

        # Check for game over
        if not game.is_active() and not paused:
            if game.turn_count > 0:  # Only print once
                print("\n" + "=" * 60)
                print("GAME OVER!")
                print("=" * 60)
                print(f"\n{game.game_over_reason}\n")
                print("Final Stats:")
                print(
                    f"  Blue Team: {game.player1.score} points, "
                    f"{int(game.player1.health)} HP"
                )
                print(
                    f"  Red Team:  {game.player2.score} points, "
                    f"{int(game.player2.health)} HP"
                )
                print(f"  Total Turns: {game.turn_count}")
                print("\nPress R to restart or Q to quit")
                print("=" * 60)
                print()

        # Render
        renderer.render_game(game)

        # Update display
        pygame.display.flip()
        clock.tick(current_fps)

    # Cleanup
    pygame.quit()
    print("\nThanks for watching the AI battle!")
    print("Game closed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
