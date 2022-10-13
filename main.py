from driver import Driver
import mss
from image_helper import find_completed_image_tiles, find_game_area, split_game_image, tile_is_blank
from models.game_board import GameBoard
from models.game_tile import GameTile
from PIL import Image
from typing import List


def get_game_tile_images(sct: mss.mss, columns: int) -> List[Image.Image]:
    game_area = find_game_area(sct)
    return split_game_image(game_area, columns)


def get_current_game_state(sct: mss.mss, columns: int) -> GameBoard:
    image_tiles = get_game_tile_images(sct, columns)
    game_tiles = [GameTile(x) for x in image_tiles if not tile_is_blank(x)]
    return GameBoard(game_tiles)


def main():
    # Open the puzzle
    puzzle_url = 'https://slidingtiles.com/en/puzzle/play/food/3665-tray-of-poultry-eggs#3x3F'
    with Driver('data/webdrivers/geckodriver/geckodriver', fullscreen=True) as driver:
        driver.go(puzzle_url)
        driver.click('#start-solve-button')

        # Open the screenshot utility
        with mss.mss() as sct:
            # This should probably be pulled from the site itself
            columns = 3

            # This is the current board
            game_board = get_current_game_state(sct, columns)

            completed_image_tiles = find_completed_image_tiles(game_board, columns)
            completed_game_tiles = [GameTile(x) for x in completed_image_tiles]

            # This is the goal board
            complete_game_board = GameBoard(completed_game_tiles)


if __name__ == '__main__':
    main()
