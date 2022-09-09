#!/usr/bin/env python3

import csv
import random
import string
import sdrdle_tx
import time
from PIL import Image, ImageDraw, ImageFont

TILE_SPACING = 80
TILE_SIZE = 70
FONT_SIZE = 50
COLORS = (128, 208, 255)

TITLE_FONT = ImageFont.truetype("FreeSansBold.ttf", FONT_SIZE * 3 // 2)
TILE_FONT = ImageFont.truetype("FreeSansBold.ttf", FONT_SIZE)
KEY_FONT = ImageFont.truetype("FreeSansBold.ttf", FONT_SIZE * 3 // 5)

WIDTH = TILE_SPACING * 6
HEIGHT = TILE_SPACING * 12


def score(target, guess):
    target_letters = list(target)
    result = [0] * len(target)

    for i in range(len(target)):
        if guess[i] == target_letters[i]:
            target_letters[i] = " "
            result[i] = 2

    for i in range(len(target)):
        if result[i] == 2:
            continue
        if guess[i] in target_letters:
            index = target_letters.index(guess[i])
            target_letters[index] = " "
            result[i] = 1

    return result


def draw_key(draw, center, letter, score):
    center_x, center_y = center

    rect = [
        (center_x - TILE_SIZE // 4, center_y - TILE_SIZE // 2),
        (center_x + TILE_SIZE // 4, center_y + TILE_SIZE // 2)
    ]

    text_x, text_y = draw.textsize(letter.upper(), font=KEY_FONT)
    if score == -1:
        bg_color = 0
        text_color = 255
    else:
        bg_color = COLORS[score]
        text_color = 0

    draw.rectangle(xy=rect, fill=bg_color, outline=255, width=4)
    draw.text((center_x - (text_x // 2), center_y - (text_y // 2)), letter.upper(), font=KEY_FONT, fill=text_color)


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
    letters = {letter: -1 for letter in string.ascii_lowercase}

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

            if guess[col] in letters:
                if scores[col] > letters[guess[col]]:
                    letters[guess[col]] = scores[col]

    keyboard = [
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm"
    ]
    row_offsets = [1.5, 2.0, 3.0]

    for row, keyboard_row in enumerate(keyboard):
        center_y = TILE_SPACING * (row + 9.5)
        for col, letter in enumerate(keyboard_row):
            center_x = TILE_SPACING * (col + row_offsets[row]) // 2
            draw_key(draw, (center_x, center_y), letter, letters[letter])


with open("words1.txt") as f:
    words1 = f.read().split()

with open("words2.txt") as f:
    words2 = f.read().split()

allowed = set(words1 + words2)

target = random.choice(words1)
guesses = []

fp = open("aprs.log", newline="", encoding="iso-8859-1")
reader = csv.DictReader(fp)
for row in reader:
    pass

for _ in range(6):
    while True:
        try:
            row = next(reader)
            source, comment = row["source"], row["comment"]
            print(source, comment)

            guess = comment.lower()
            if guess in allowed:
                guesses.append(guess)
                break
            else:
                print("Not in word list")

        except StopIteration:
            time.sleep(0.1)

    image = Image.new(mode="L", size=(WIDTH, HEIGHT), color=0)
    draw = ImageDraw.Draw(image)

    draw_board(draw, target, guesses)

    image.save("sdrdle.png")

    tb = sdrdle_tx.sdrdle_tx()
    tb.run()

    if guess == target:
        break
