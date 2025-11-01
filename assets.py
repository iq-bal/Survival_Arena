"""
Asset loader for the AI vs AI Survival Arena
Loads all PNG images from the icons folder
"""

import pygame
import os


class AssetLoader:
    """Loads and manages all game assets (images)."""

    def __init__(self):
        """Initialize the asset loader."""
        self.base_path = os.path.dirname(__file__)
        self.icons_path = os.path.join(self.base_path, "icons")

        # Storage for loaded assets
        self.entities = {}
        self.ui_icons = {}
        self.legend_icons = {}

        # Load all assets
        self._load_all_assets()

    def _load_image(self, filepath, size=None):
        """
        Load an image file and optionally scale it.

        Args:
            filepath: Path to the image file
            size: Optional tuple (width, height) to scale the image

        Returns:
            Loaded pygame Surface, or None if file doesn't exist
        """
        try:
            image = pygame.image.load(filepath).convert_alpha()
            if size:
                image = pygame.transform.smoothscale(image, size)
            return image
        except (pygame.error, FileNotFoundError) as e:
            print(f"Warning: Could not load {filepath}: {e}")
            return None

    def _load_all_assets(self):
        """Load all game assets from the icons folder."""
        # Load entity icons (game grid size)
        entities_path = os.path.join(self.icons_path, "entities")
        self.entities = {
            "player_blue": self._load_image(os.path.join(entities_path, "player_blue.png"), (30, 30)),
            "player_red": self._load_image(os.path.join(entities_path, "player_red.png"), (30, 30)),
            "ally_blue": self._load_image(os.path.join(entities_path, "ally_blue.png"), (28, 28)),
            "ally_red": self._load_image(os.path.join(entities_path, "ally_red.png"), (28, 28)),
            "enemy": self._load_image(os.path.join(entities_path, "enemy.png"), (28, 28)),
            "health_pack": self._load_image(os.path.join(entities_path, "health_pack.png"), (28, 28)),
            "coin": self._load_image(os.path.join(entities_path, "coin.png"), (28, 28)),
            "wall": self._load_image(os.path.join(entities_path, "wall.png"), (30, 30)),
        }

        # Load UI icons (stat card size)
        ui_path = os.path.join(self.icons_path, "ui")
        self.ui_icons = {
            "clock": self._load_image(os.path.join(ui_path, "icon_clock.png"), (20, 20)),
            "heart": self._load_image(os.path.join(ui_path, "icon_heart.png"), (20, 20)),
            "skull": self._load_image(os.path.join(ui_path, "icon_skull.png"), (20, 20)),
            "gamepad": self._load_image(os.path.join(ui_path, "icon_gamepad.png"), (35, 35)),
            "brain": self._load_image(os.path.join(ui_path, "icon_brain.png"), (20, 20)),
            "star": self._load_image(os.path.join(ui_path, "icon_star.png"), (18, 18)),
            "restart": self._load_image(os.path.join(ui_path, "icon_restart.png"), (18, 18)),
        }

        # Load legend icons (small size for sidebar)
        legend_path = os.path.join(self.icons_path, "legend")
        self.legend_icons = {
            "player_blue": self._load_image(os.path.join(legend_path, "player_blue.png"), (16, 16)),
            "player_red": self._load_image(os.path.join(legend_path, "player_red.png"), (16, 16)),
            "ally_blue": self._load_image(os.path.join(legend_path, "ally_blue.png"), (16, 16)),
            "ally_red": self._load_image(os.path.join(legend_path, "ally_red.png"), (16, 16)),
            "enemy": self._load_image(os.path.join(legend_path, "enemy.png"), (16, 16)),
            "health_pack": self._load_image(os.path.join(legend_path, "health_pack.png"), (16, 16)),
            "coin": self._load_image(os.path.join(legend_path, "coin.png"), (16, 16)),
            "wall": self._load_image(os.path.join(legend_path, "wall.png"), (16, 16)),
        }

    def get_entity(self, name):
        """Get an entity image by name."""
        return self.entities.get(name)

    def get_ui_icon(self, name):
        """Get a UI icon by name."""
        return self.ui_icons.get(name)

    def get_legend_icon(self, name):
        """Get a legend icon by name."""
        return self.legend_icons.get(name)


# Global asset loader instance (initialized when module is imported)
_asset_loader = None


def get_assets():
    """Get the global asset loader instance."""
    global _asset_loader
    if _asset_loader is None:
        # Initialize pygame if not already done
        if not pygame.get_init():
            pygame.init()
        _asset_loader = AssetLoader()
    return _asset_loader
