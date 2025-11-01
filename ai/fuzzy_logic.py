"""
Fuzzy Logic Decision System
Used by AI players to make strategic decisions based on game state.
"""

from constants import ACTIONS


class FuzzyLogic:
    """Fuzzy logic decision-making for AI players."""

    @staticmethod
    def triangular_membership(value, left, peak, right):
        """
        Calculate triangular membership function.

        Args:
            value: input value
            left: left boundary
            peak: peak value (membership = 1.0)
            right: right boundary

        Returns:
            Membership value between 0.0 and 1.0
        """
        if value <= left or value >= right:
            return 0.0
        elif value == peak:
            return 1.0
        elif value < peak:
            return (value - left) / (peak - left)
        else:
            return (right - value) / (right - peak)

    @staticmethod
    def trapezoidal_membership(value, left, left_peak, right_peak, right):
        """
        Calculate trapezoidal membership function.

        Args:
            value: input value
            left: left boundary
            left_peak: left peak (membership = 1.0 starts)
            right_peak: right peak (membership = 1.0 ends)
            right: right boundary

        Returns:
            Membership value between 0.0 and 1.0
        """
        if value <= left or value >= right:
            return 0.0
        elif left_peak <= value <= right_peak:
            return 1.0
        elif value < left_peak:
            return (value - left) / (left_peak - left)
        else:
            return (right - value) / (right - right_peak)

    @staticmethod
    def health_membership(health):
        """
        Calculate fuzzy membership for health levels.

        Returns:
            Dictionary with LOW, MEDIUM, HIGH membership values
        """
        low = FuzzyLogic.trapezoidal_membership(health, 0, 0, 20, 35)
        medium = FuzzyLogic.triangular_membership(health, 30, 50, 70)
        high = FuzzyLogic.trapezoidal_membership(health, 65, 80, 100, 100)

        return {"LOW": low, "MEDIUM": medium, "HIGH": high}

    @staticmethod
    def score_membership(score, max_score=500):
        """
        Calculate fuzzy membership for score levels.

        Returns:
            Dictionary with LOW, MEDIUM, HIGH membership values
        """
        # Normalize score to 0-100 scale
        normalized = (score / max_score) * 100

        low = FuzzyLogic.trapezoidal_membership(normalized, 0, 0, 20, 40)
        medium = FuzzyLogic.triangular_membership(normalized, 30, 50, 70)
        high = FuzzyLogic.trapezoidal_membership(normalized, 60, 80, 100, 100)

        return {"LOW": low, "MEDIUM": medium, "HIGH": high}

    @staticmethod
    def distance_membership(distance):
        """
        Calculate fuzzy membership for distance levels.

        Returns:
            Dictionary with NEAR, MEDIUM, FAR membership values
        """
        near = FuzzyLogic.trapezoidal_membership(distance, 0, 0, 2, 4)
        medium = FuzzyLogic.triangular_membership(distance, 3, 5, 8)
        far = FuzzyLogic.trapezoidal_membership(distance, 7, 10, 20, 20)

        return {"NEAR": near, "MEDIUM": medium, "FAR": far}

    @staticmethod
    def apply_fuzzy_rules(health, score, nearest_enemy_dist, nearest_resource_dist):
        """
        Apply fuzzy rules to determine action.

        Fuzzy Rules:
        1. IF health LOW AND enemy NEAR → FLEE_ENEMY (weight: max)
        2. IF health LOW AND enemy FAR → SEEK_HEALTH
        3. IF health HIGH AND score LOW → COLLECT_COINS
        4. IF health HIGH AND score HIGH → AGGRESSIVE_PLAY
        5. IF health MEDIUM → DEFENSIVE_PLAY

        Args:
            health: current health (0-100)
            score: current score
            nearest_enemy_dist: distance to nearest enemy
            nearest_resource_dist: distance to nearest resource

        Returns:
            Best action based on fuzzy logic
        """
        # Calculate memberships
        health_fuzzy = FuzzyLogic.health_membership(health)
        score_fuzzy = FuzzyLogic.score_membership(score)
        enemy_dist_fuzzy = FuzzyLogic.distance_membership(nearest_enemy_dist)
        resource_dist_fuzzy = FuzzyLogic.distance_membership(nearest_resource_dist)

        # Initialize action strengths
        action_strengths = {
            ACTIONS["FLEE_ENEMY"]: 0.0,
            ACTIONS["SEEK_HEALTH"]: 0.0,
            ACTIONS["COLLECT_COINS"]: 0.0,
            ACTIONS["AGGRESSIVE_PLAY"]: 0.0,
            ACTIONS["DEFENSIVE_PLAY"]: 0.0,
            ACTIONS["COLLECT_RESOURCES"]: 0.0,
        }

        # Rule 1: IF health LOW AND enemy NEAR → FLEE_ENEMY
        rule1_strength = min(health_fuzzy["LOW"], enemy_dist_fuzzy["NEAR"])
        action_strengths[ACTIONS["FLEE_ENEMY"]] = max(
            action_strengths[ACTIONS["FLEE_ENEMY"]], rule1_strength * 1.5
        )  # High priority

        # Rule 2: IF health LOW AND enemy FAR → SEEK_HEALTH
        rule2_strength = min(health_fuzzy["LOW"], enemy_dist_fuzzy["FAR"])
        action_strengths[ACTIONS["SEEK_HEALTH"]] = max(
            action_strengths[ACTIONS["SEEK_HEALTH"]], rule2_strength
        )

        # Rule 3: IF health HIGH AND score LOW → COLLECT_COINS
        rule3_strength = min(health_fuzzy["HIGH"], score_fuzzy["LOW"])
        action_strengths[ACTIONS["COLLECT_COINS"]] = max(
            action_strengths[ACTIONS["COLLECT_COINS"]], rule3_strength
        )

        # Rule 4: IF health HIGH AND score HIGH → AGGRESSIVE_PLAY
        rule4_strength = min(health_fuzzy["HIGH"], score_fuzzy["HIGH"])
        action_strengths[ACTIONS["AGGRESSIVE_PLAY"]] = max(
            action_strengths[ACTIONS["AGGRESSIVE_PLAY"]], rule4_strength
        )

        # Rule 5: IF health MEDIUM → DEFENSIVE_PLAY
        rule5_strength = health_fuzzy["MEDIUM"]
        action_strengths[ACTIONS["DEFENSIVE_PLAY"]] = max(
            action_strengths[ACTIONS["DEFENSIVE_PLAY"]], rule5_strength
        )

        # Rule 6: IF health LOW AND enemy MEDIUM → COLLECT_RESOURCES (cautiously)
        rule6_strength = min(health_fuzzy["LOW"], enemy_dist_fuzzy["MEDIUM"])
        action_strengths[ACTIONS["COLLECT_RESOURCES"]] = max(
            action_strengths[ACTIONS["COLLECT_RESOURCES"]], rule6_strength * 0.7
        )

        # Rule 7: IF health MEDIUM AND score LOW → COLLECT_RESOURCES
        rule7_strength = min(health_fuzzy["MEDIUM"], score_fuzzy["LOW"])
        action_strengths[ACTIONS["COLLECT_RESOURCES"]] = max(
            action_strengths[ACTIONS["COLLECT_RESOURCES"]], rule7_strength
        )

        # Rule 8: IF enemy NEAR AND health MEDIUM → DEFENSIVE_PLAY (boost)
        rule8_strength = min(enemy_dist_fuzzy["NEAR"], health_fuzzy["MEDIUM"])
        action_strengths[ACTIONS["DEFENSIVE_PLAY"]] = max(
            action_strengths[ACTIONS["DEFENSIVE_PLAY"]], rule8_strength * 1.2
        )

        # Defuzzification: Return action with maximum membership
        best_action = max(action_strengths, key=action_strengths.get)

        return best_action

    @staticmethod
    def decide_action(health, score, nearest_enemy_dist, nearest_resource_dist):
        """
        Main decision function for AI players.

        Args:
            health: current health (0-100)
            score: current score
            nearest_enemy_dist: distance to nearest enemy
            nearest_resource_dist: distance to nearest resource

        Returns:
            Action string (from ACTIONS constants)
        """
        return FuzzyLogic.apply_fuzzy_rules(
            health, score, nearest_enemy_dist, nearest_resource_dist
        )
