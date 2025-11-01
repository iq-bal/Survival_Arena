"""
A* Pathfinding Algorithm
Used by ally bots to navigate to resources while avoiding obstacles.
"""

import heapq


class Node:
    """Node class for A* pathfinding."""

    def __init__(self, position, parent=None):
        self.position = position  # (x, y)
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost from current to goal
        self.f = 0  # Total cost (g + h)

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return hash(self.position)


class AStarPathfinder:
    """A* pathfinding implementation for navigating the grid."""

    @staticmethod
    def manhattan_distance(pos1, pos2):
        """Calculate Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    @staticmethod
    def get_neighbors(position, grid_size):
        """Get valid neighboring positions (4-directional movement)."""
        x, y = position
        neighbors = []

        # Check all 4 directions: up, down, left, right
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                neighbors.append((new_x, new_y))

        return neighbors

    @staticmethod
    def find_path(start, goal, obstacles, grid_size):
        """
        Find optimal path from start to goal using A* algorithm.

        Args:
            start: (x, y) starting position
            goal: (x, y) goal position
            obstacles: set of (x, y) positions that are blocked
            grid_size: size of the grid (assumes square grid)

        Returns:
            List of (x, y) positions from start to goal, or [start] if no path found
        """
        # If start equals goal, return immediately
        if start == goal:
            return [start]

        # Initialize start and goal nodes
        start_node = Node(start)
        goal_node = Node(goal)

        # Initialize open and closed lists
        open_list = []
        closed_set = set()

        heapq.heappush(open_list, start_node)

        while open_list:
            # Get node with lowest f score
            current_node = heapq.heappop(open_list)

            # Add to closed set
            closed_set.add(current_node.position)

            # Check if we reached the goal
            if current_node.position == goal_node.position:
                # Reconstruct path
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Reverse to get start -> goal

            # Get neighbors
            neighbors = AStarPathfinder.get_neighbors(current_node.position, grid_size)

            for neighbor_pos in neighbors:
                # Skip if obstacle or already visited
                if neighbor_pos in obstacles or neighbor_pos in closed_set:
                    continue

                # Create neighbor node
                neighbor_node = Node(neighbor_pos, current_node)

                # Calculate costs
                neighbor_node.g = current_node.g + 1  # Each step costs 1
                neighbor_node.h = AStarPathfinder.manhattan_distance(
                    neighbor_pos, goal_node.position
                )
                neighbor_node.f = neighbor_node.g + neighbor_node.h

                # Check if neighbor is already in open list with lower f
                skip = False
                for open_node in open_list:
                    if (
                        open_node.position == neighbor_node.position
                        and open_node.f <= neighbor_node.f
                    ):
                        skip = True
                        break

                if not skip:
                    heapq.heappush(open_list, neighbor_node)

        # No path found, return start position
        return [start]

    @staticmethod
    def get_next_move(start, goal, obstacles, grid_size):
        """
        Get the next move towards goal using A*.

        Args:
            start: (x, y) starting position
            goal: (x, y) goal position
            obstacles: set of (x, y) positions that are blocked
            grid_size: size of the grid

        Returns:
            (x, y) next position to move to, or start if no path
        """
        path = AStarPathfinder.find_path(start, goal, obstacles, grid_size)

        # Return next step in path, or stay in place
        if len(path) > 1:
            return path[1]
        return start
