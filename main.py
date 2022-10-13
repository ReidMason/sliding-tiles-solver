from driver import Driver
import mss
from image_helper import find_game_area, split_game_image
from models.game_board import GameBoard
from models.game_tile import GameTile
from PIL import Image
from typing import List


def get_game_tile_images(sct: mss.mss, columns: int) -> List[Image.Image]:
    game_area = find_game_area(sct)
    return split_game_image(game_area, columns)


def get_current_game_state(sct: mss.mss, columns: int) -> GameBoard:
    image_tiles = get_game_tile_images(sct, columns)
    game_tiles = [GameTile(x) for x in image_tiles]
    return GameBoard(game_tiles)


def get_completed_game_board(current_game_board: GameBoard) -> GameBoard:
    completed_image_tiles = current_game_board.find_completed_image_tiles()
    return GameBoard([GameTile(x) for x in completed_image_tiles])


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

            # This is the current and completed board states
            game_board = get_current_game_state(sct, columns)
            complete_game_board = get_completed_game_board(game_board)


if __name__ == '__main__':
    main()
