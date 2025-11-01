"""
Minimax Algorithm with Alpha-Beta Pruning
Used by enemy agents to choose optimal targets between two players.
"""

import math
from ai.astar import AStarPathfinder


class MinimaxAI:
    """Minimax decision-making for enemy agents."""

    @staticmethod
    def manhattan_distance(pos1, pos2):
        """Calculate Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    @staticmethod
    def evaluate_position(enemy_pos, player_pos, player_health):
        """
        Evaluate the desirability of targeting a specific player.

        Score = -(distance) + (100 - player_health)/10
        Lower distance + lower player health = better score (higher value)

        Args:
            enemy_pos: (x, y) position of the enemy
            player_pos: (x, y) position of the player
            player_health: current health of the player

        Returns:
            Evaluation score (higher is better for enemy)
        """
        distance = MinimaxAI.manhattan_distance(enemy_pos, player_pos)

        # Prefer closer targets and weaker targets
        score = -distance + (100 - player_health) / 10

        return score

    @staticmethod
    def get_valid_moves(position, obstacles, grid_size):
        """
        Get all valid moves from a position.

        Args:
            position: (x, y) current position
            obstacles: set of (x, y) obstacle positions
            grid_size: size of the grid

        Returns:
            List of valid (x, y) positions to move to
        """
        x, y = position
        moves = []

        # 4-directional movement: up, down, left, right
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if (
                0 <= new_x < grid_size
                and 0 <= new_y < grid_size
                and (new_x, new_y) not in obstacles
            ):
                moves.append((new_x, new_y))

        # If no valid moves, stay in place
        if not moves:
            moves.append(position)

        return moves

    @staticmethod
    def minimax(
        enemy_pos,
        player1_pos,
        player2_pos,
        player1_health,
        player2_health,
        obstacles,
        grid_size,
        depth,
        alpha,
        beta,
        is_maximizing,
    ):
        """
        Minimax algorithm with alpha-beta pruning.

        Args:
            enemy_pos: (x, y) enemy position
            player1_pos: (x, y) player 1 position
            player2_pos: (x, y) player 2 position
            player1_health: player 1 health
            player2_health: player 2 health
            obstacles: set of obstacle positions
            grid_size: grid size
            depth: remaining search depth
            alpha: alpha value for pruning
            beta: beta value for pruning
            is_maximizing: True if maximizing player (enemy), False if minimizing (players)

        Returns:
            Tuple of (score, best_move)
        """
        # Base case: depth reached
        if depth == 0:
            # Evaluate both targets and return best score
            score1 = MinimaxAI.evaluate_position(enemy_pos, player1_pos, player1_health)
            score2 = MinimaxAI.evaluate_position(enemy_pos, player2_pos, player2_health)
            return max(score1, score2), enemy_pos

        if is_maximizing:
            # Enemy's turn (maximizing)
            max_eval = -math.inf
            best_move = enemy_pos

            valid_moves = MinimaxAI.get_valid_moves(enemy_pos, obstacles, grid_size)

            for move in valid_moves:
                # Recursively evaluate this move
                eval_score, _ = MinimaxAI.minimax(
                    move,
                    player1_pos,
                    player2_pos,
                    player1_health,
                    player2_health,
                    obstacles,
                    grid_size,
                    depth - 1,
                    alpha,
                    beta,
                    False,
                )

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff

            return max_eval, best_move
        else:
            # Players' turn (minimizing - they try to escape)
            min_eval = math.inf

            # Simulate both players trying to escape
            player1_moves = MinimaxAI.get_valid_moves(player1_pos, obstacles, grid_size)
            player2_moves = MinimaxAI.get_valid_moves(player2_pos, obstacles, grid_size)

            # Try a sample of moves (to keep computation reasonable)
            for p1_move in player1_moves[:2]:  # Limit moves to keep it fast
                for p2_move in player2_moves[:2]:
                    eval_score, _ = MinimaxAI.minimax(
                        enemy_pos,
                        p1_move,
                        p2_move,
                        player1_health,
                        player2_health,
                        obstacles,
                        grid_size,
                        depth - 1,
                        alpha,
                        beta,
                        True,
                    )

                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break  # Alpha cutoff

                if beta <= alpha:
                    break

            return min_eval, enemy_pos

    @staticmethod
    def choose_target_and_move(
        enemy_pos, player1_pos, player2_pos, player1_health, player2_health, obstacles, grid_size, depth=3
    ):
        """
        Choose the best target and move for an enemy using Minimax.

        Args:
            enemy_pos: (x, y) enemy position
            player1_pos: (x, y) player 1 position
            player2_pos: (x, y) player 2 position
            player1_health: player 1 health
            player2_health: player 2 health
            obstacles: set of obstacle positions
            grid_size: grid size
            depth: search depth (default 3)

        Returns:
            Tuple of (best_target_pos, best_move)
        """
        # Evaluate both players
        score1 = MinimaxAI.evaluate_position(enemy_pos, player1_pos, player1_health)
        score2 = MinimaxAI.evaluate_position(enemy_pos, player2_pos, player2_health)

        # Choose target with better score
        if score1 >= score2:
            target = player1_pos
        else:
            target = player2_pos

        # Use minimax to find best move
        _, best_move = MinimaxAI.minimax(
            enemy_pos,
            player1_pos,
            player2_pos,
            player1_health,
            player2_health,
            obstacles,
            grid_size,
            depth,
            -math.inf,
            math.inf,
            True,
        )

        return target, best_move

    @staticmethod
    def get_next_move(enemy_pos, target_pos, obstacles, grid_size):
        """
        Get next move towards target using A* pathfinding.

        Args:
            enemy_pos: (x, y) enemy position
            target_pos: (x, y) target position
            obstacles: set of obstacle positions
            grid_size: grid size

        Returns:
            (x, y) next position to move to
        """
        return AStarPathfinder.get_next_move(enemy_pos, target_pos, obstacles, grid_size)
