#!/usr/bin/env python3

import random
import sdrdle_tx
from PIL import Image, ImageDraw, ImageFont

TILE_SPACING = 80
TILE_SIZE = 70
FONT_SIZE = 50
COLORS = (128, 208, 255)

TITLE_FONT = ImageFont.truetype("FreeSansBold.ttf", FONT_SIZE * 3 // 2)
TILE_FONT = ImageFont.truetype("FreeSansBold.ttf", FONT_SIZE)

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


def draw_tile(draw, center, letter, score):
    center_x, center_y = center

    rect = [
        (center_x - TILE_SIZE // 2, center_y - TILE_SIZE // 2),
        (center_x + TILE_SIZE // 2, center_y + TILE_SIZE // 2)
    ]

    if letter == " ":
        draw.rectangle(xy=rect, outline=255, width=4)
    else:
        draw.rectangle(xy=rect, fill=COLORS[score], outline=255, width=4)
        text_x, text_y = draw.textsize(letter.upper(), font=TILE_FONT)
        draw.text((center_x - (text_x // 2), center_y - (text_y // 2)), letter.upper(), font=TILE_FONT, fill=0)


def draw_board(draw, target, guesses):
    guesses = guesses + ["     "] * (6 - len(guesses))

    title = "SDRdle"
    text_x, text_y = draw.textsize(title, font=TITLE_FONT)
    draw.text((WIDTH // 2 - (text_x // 2), TILE_SPACING * 3 // 2 - (text_y // 2)), title, font=TITLE_FONT, fill=255)

    for row in range(6):
        center_y = TILE_SPACING * (row + 3)
        guess = guesses[row]
        scores = score(target, guess)
        for col in range(5):
            center_x = (WIDTH // 2) + TILE_SPACING * (col - 2)
            draw_tile(draw, (center_x, center_y), guess[col], scores[col])


with open("words1.txt") as f:
    words1 = f.read().split()

with open("words2.txt") as f:
    words2 = f.read().split()

allowed = set(words1 + words2)

target = random.choice(words1)
guesses = []

for _ in range(6):
    while True:
        guess = input("Guess: ").lower()
        if guess in allowed:
            guesses.append(guess)
            break
        else:
            print("Not in word list")

    image = Image.new(mode="L", size=(WIDTH, HEIGHT), color=0)
    draw = ImageDraw.Draw(image)

    draw_board(draw, target, guesses)

    image.save("sdrdle.png")

    tb = sdrdle_tx.sdrdle_tx()
    tb.run()
