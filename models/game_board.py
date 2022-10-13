from typing import List
from models.game_tile import GameTile
from utils import list_to_2d_array
from PIL import Image
import os
from image_helper import split_game_image, images_are_similar
import math


class GameBoard:
    def __init__(self, game_tiles: List[GameTile]) -> None:
        self.game_tiles: List[List] = list_to_2d_array(game_tiles)

    @property
    def game_tiles_list(self) -> List[GameTile]:
        return [item for sublist in self.game_tiles for item in sublist]

    @property
    def columns(self) -> int:
        return math.ceil(math.sqrt(len(self.game_tiles_list)))

    def find_completed_image_tiles(self) -> List[Image.Image]:
        base_path = "data/completed_images"
        for file in [x for x in os.listdir(base_path) if x.endswith(".webp")]:
            image_path = os.path.join(base_path, file)
            reference_image = Image.open(image_path).convert('RGB')
            reference_images = split_game_image(reference_image, self.columns)

            matches = 0
            for img_1 in [x.image for x in self.game_tiles_list]:
                for img_2 in reference_images:
                    if images_are_similar(img_1, img_2):
                        matches += 1

            if matches >= 8:
                return reference_images
