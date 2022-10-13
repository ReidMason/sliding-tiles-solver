from itertools import product
import os
from typing import List, Tuple
from PIL import Image
import io
import mss
from utils import colours_match, images_are_similar

target_colour = (66, 141, 154)


def screenshot(sct: mss.mss) -> Image.Image:
    monitor = sct.monitors[1]
    sct_img = sct.grab(monitor)
    png = mss.tools.to_png(sct_img.rgb, sct_img.size)

    return Image.open(io.BytesIO(png))


def find_x_boundaries(image: Image.Image) -> List[int]:
    output = []
    midheight = int(image.height / 2)
    colour_span = 0
    for x in range(image.width):
        position = (x, midheight)
        pixel_colour = image.getpixel(position)

        if colours_match(pixel_colour, target_colour):
            colour_span += 1
            image.putpixel(position, (255, 0, 0))
        elif colour_span > 50:
            if len(output) == 0:
                output.append(x)
            else:
                output.append(x - colour_span)
            colour_span = 0
        else:
            colour_span = 0

    return output


def find_y_boundaries(image: Image.Image) -> List[int]:
    output = []
    midwidth = int(image.width / 2)
    colour_span = 0
    for y in range(image.height):
        position = (midwidth, y)
        pixel_colour = image.getpixel(position)

        if colours_match(pixel_colour, target_colour):
            colour_span += 1
            image.putpixel(position, (255, 0, 0))
        elif colour_span > 50:
            if len(output) == 0:
                output.append(y)
            else:
                output.append(y - colour_span)
            colour_span = 0
        else:
            colour_span = 0

    return output


def find_game_area(sct: mss.mss) -> Image.Image:
    image = screenshot(sct).convert('RGB')
    x_boundaies = find_x_boundaries(image)
    y_boundaries = find_y_boundaries(image)

    boundary = (x_boundaies[0], y_boundaries[0], x_boundaies[1], y_boundaries[1])
    return image.crop(boundary).resize((720, 720))


def split_game_image(image: Image.Image, columns: int) -> List[Image.Image]:
    w, h = image.size
    d = int(image.width / columns)

    images = []
    grid = product(range(0, h-h%d, d), range(0, w-w%d, d))
    for i, j in grid:
        box = (j, i, j+d, i+d)
        images.append(image.crop(box))

    return images


def find_completed_image_tiles(game_tiles: List[Image.Image], columns: int) -> Tuple[List[Image.Image], List[Image.Image]]:
    base_path = "data/completed_images"
    for file in [x for x in os.listdir(base_path) if x.endswith(".webp")]:
        image_path = os.path.join(base_path, file)
        reference_image = Image.open(image_path).convert('RGB')
        reference_images = split_game_image(reference_image, columns)

        matched_images = []
        for img_1 in game_tiles:
            for img_2 in reference_images:
                if images_are_similar(img_1, img_2):
                    matched_images.append(img_1)

        if len(matched_images) >= 8:
            return (reference_images, matched_images)