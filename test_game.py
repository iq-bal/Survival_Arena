#!/usr/bin/env python3
"""
Quick test script to verify game initialization and basic functionality.
"""

import sys


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        import constants
        print("  ✓ constants")

        import entities
        print("  ✓ entities")

        import game
        print("  ✓ game")

        from ai.astar import AStarPathfinder
        print("  ✓ ai.astar")

        from ai.minimax import MinimaxAI
        print("  ✓ ai.minimax")

        from ai.fuzzy_logic import FuzzyLogic
        print("  ✓ ai.fuzzy_logic")

        print("\nAll imports successful!")
        return True
    except Exception as e:
        print(f"\n✗ Import failed: {e}")
        return False


def test_game_initialization():
    """Test game initialization."""
    print("\nTesting game initialization...")
    try:
        from game import SurvivalArenaGame

        game = SurvivalArenaGame()
        print(f"  ✓ Game created")
        print(f"  ✓ Player 1: {game.player1.team} at {game.player1.position}")
        print(f"  ✓ Player 2: {game.player2.team} at {game.player2.position}")
        print(f"  ✓ Allies: {len(game.allies)}")
        print(f"  ✓ Enemies: {len(game.enemies)}")
        print(f"  ✓ Obstacles: {len(game.obstacles)}")
        print(f"  ✓ Resources: {len(game.resources)}")

        print("\nGame initialization successful!")
        return True
    except Exception as e:
        print(f"\n✗ Initialization failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_ai_algorithms():
    """Test AI algorithms."""
    print("\nTesting AI algorithms...")
    try:
        from ai.astar import AStarPathfinder
        from ai.minimax import MinimaxAI
        from ai.fuzzy_logic import FuzzyLogic

        # Test A*
        path = AStarPathfinder.find_path((0, 0), (5, 5), set(), 20)
        print(f"  ✓ A* pathfinding: {len(path)} steps")

        # Test Minimax
        target, move = MinimaxAI.choose_target_and_move(
            (10, 10), (5, 5), (15, 15), 100, 50, set(), 20, 2
        )
        print(f"  ✓ Minimax targeting: target={target}, move={move}")

        # Test Fuzzy Logic
        action = FuzzyLogic.decide_action(50, 100, 5, 3)
        print(f"  ✓ Fuzzy logic decision: {action}")

        print("\nAll AI algorithms working!")
        return True
    except Exception as e:
        print(f"\n✗ AI algorithm test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_turn_execution():
    """Test executing a few game turns."""
    print("\nTesting turn execution...")
    try:
        from game import SurvivalArenaGame

        game = SurvivalArenaGame()

        for i in range(5):
            game.execute_turn()
            print(f"  ✓ Turn {i + 1}: Blue HP={int(game.player1.health)}, Red HP={int(game.player2.health)}")

        print("\nTurn execution successful!")
        return True
    except Exception as e:
        print(f"\n✗ Turn execution failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("AI vs AI Survival Arena - Test Suite")
    print("=" * 60)

    tests = [
        test_imports,
        test_game_initialization,
        test_ai_algorithms,
        test_turn_execution,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test crashed: {e}")
            import traceback

            traceback.print_exc()
            results.append(False)

        print()

    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if all(results):
        print("\n✓ All tests passed! Game is ready to run.")
        print("\nTo start the game, run:")
        print("  python3 main.py")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
