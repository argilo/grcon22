#!/usr/bin/env python3

import random
from PIL import Image, ImageDraw, ImageFont

TILE_SPACING = 80
TILE_SIZE = 70
FONT_SIZE = 50

WIDTH = TILE_SPACING * 6
HEIGHT = TILE_SPACING * 8


def draw_board(draw, target, guesses):
    while len(guesses) < 6:
        guesses.append("     ")

    title_font = ImageFont.truetype("FreeSansBold.ttf", FONT_SIZE * 3 // 2)
    tile_font = ImageFont.truetype("FreeSansBold.ttf", FONT_SIZE)

    title = "SDRdle"
    text_x, text_y = draw.textsize(title, font=title_font)
    draw.text((WIDTH // 2 - (text_x // 2), TILE_SPACING * 3 // 4 - (text_y // 2)), title, font=title_font, fill=255)

    for row in range(6):
        center_y = TILE_SPACING * (row + 2)
        for col in range(5):
            center_x = (WIDTH // 2) + TILE_SPACING * (col - 2)
            rect = [
                (center_x - TILE_SIZE // 2, center_y - TILE_SIZE // 2),
                (center_x + TILE_SIZE // 2, center_y + TILE_SIZE // 2)
            ]

            letter = guesses[row][col]

            if letter == " ":
                draw.rectangle(xy=rect, width=4, outline=255)
            else:
                draw.rectangle(xy=rect, fill=255 - random.randrange(3) * 80)

            text_x, text_y = draw.textsize(letter, font=tile_font)
            draw.text((center_x - (text_x // 2), center_y - (text_y // 2)), letter, font=tile_font, fill=0)


image = Image.new(mode="L", size=(WIDTH, HEIGHT), color=0)
draw = ImageDraw.Draw(image)

draw_board(draw, "BUGGY", ["EARTH", "LOINS", "DUMPY", "CUBBY", "BUGGY"])

image.save("sdrdle.png")
