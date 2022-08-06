#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont

TILE_SPACING = 80
TILE_SIZE = 70
FONT_SIZE = 50
COLORS = (128, 208, 255)

WIDTH = TILE_SPACING * 6
HEIGHT = TILE_SPACING * 9


def score(target, guess):
    target_letters = list(target)
    result = [0] * len(target)

    for i in range(len(target)):
        if guess[i] == target_letters[i]:
            target_letters[i] = " "
            result[i] = 2

    for i in range(len(target)):
        if guess[i] in target_letters:
            index = target_letters.index(guess[i])
            target_letters[index] = " "
            result[i] = 1

    return result


def draw_board(draw, target, guesses):
    while len(guesses) < 6:
        guesses.append("     ")

    title_font = ImageFont.truetype("FreeSansBold.ttf", FONT_SIZE * 3 // 2)
    tile_font = ImageFont.truetype("FreeSansBold.ttf", FONT_SIZE)

    title = "SDRdle"
    text_x, text_y = draw.textsize(title, font=title_font)
    draw.text((WIDTH // 2 - (text_x // 2), TILE_SPACING * 3 // 2 - (text_y // 2)), title, font=title_font, fill=255)

    for row in range(6):
        center_y = TILE_SPACING * (row + 3)
        scores = score(target, guesses[row])
        for col in range(5):
            center_x = (WIDTH // 2) + TILE_SPACING * (col - 2)
            rect = [
                (center_x - TILE_SIZE // 2, center_y - TILE_SIZE // 2),
                (center_x + TILE_SIZE // 2, center_y + TILE_SIZE // 2)
            ]

            letter = guesses[row][col]

            if letter == " ":
                draw.rectangle(xy=rect, outline=255, width=4)
            else:
                draw.rectangle(xy=rect, fill=COLORS[scores[col]], outline=255, width=4)

            text_x, text_y = draw.textsize(letter, font=tile_font)
            draw.text((center_x - (text_x // 2), center_y - (text_y // 2)), letter, font=tile_font, fill=0)


image = Image.new(mode="L", size=(WIDTH, HEIGHT), color=0)
draw = ImageDraw.Draw(image)

draw_board(draw, "BUGGY", ["EARTH", "LOINS", "DUMPY", "CUBBY", "BUGGY"])

image.save("sdrdle.png")
