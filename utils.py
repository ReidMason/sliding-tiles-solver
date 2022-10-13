import logging
import math
from typing import List, Tuple

logging_level = logging.DEBUG
log_format = '%(asctime)s [%(name)s] %(message)s'
log_date_format = '%d-%m-%Y %HL%M:%S'


def create_logger(name: str) -> logging.Logger:
    logging.basicConfig(format=log_format, datefmt=log_date_format)
    logger = logging.getLogger(name)
    logger.setLevel(logging_level)
    return logger


def number_is_close(target_num: int, test_num: int, distance: int) -> bool:
    return abs(target_num - test_num) < distance


def colours_match(colour_a: Tuple[int, int, int], colour_b: Tuple[int, int, int]) -> bool:
    for value_a, value_b in zip(colour_a, colour_b):
        if not number_is_close(value_a, value_b, 2):
            return False

    return True


def list_to_2d_array(game_tiles: List[any]) -> List[List[any]]:
    columns = math.ceil(math.sqrt(len(game_tiles)))

    game_array = []
    row = []
    for tile in game_tiles:
        row.append(tile)
        if len(row) == columns:
            game_array.append(row)
            row = []

    if len(row) > 0:
        game_array.append(row)

    return game_array
