from typing import List

from models.game_tile import GameTile
from utils import list_to_2d_array

class GameBoard:
    def __init__(self, game_tiles: List[GameTile]) -> None:
        self.game_tiles: List[List] = list_to_2d_array(game_tiles) 
