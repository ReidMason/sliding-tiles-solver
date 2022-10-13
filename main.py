from driver import Driver
import mss
from image_helper import find_completed_image_tiles, find_game_area, split_game_image
from models.game_board import GameBoard
from models.game_tile import GameTile


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

            game_area = find_game_area(sct)
            game_images = split_game_image(game_area, columns)
            completed_image_tiles, image_tiles = find_completed_image_tiles(game_images, columns)

            # Create the working game board and completed game board
            game_tiles = [GameTile(x) for x in image_tiles]
            game_board = GameBoard(game_tiles)
            completed_game_tiles = [GameTile(x) for x in completed_image_tiles]
            complete_game_board = GameBoard(completed_game_tiles)


if __name__ == '__main__':
    main()
