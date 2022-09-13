#!/usr/bin/env bash

set -e

qrencode -o rickroll.png 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
qrencode -o flag.png 'Part 2: flag{2OBGfE29cR1SpOXuJpI832FyAWvNPLtC}'

for SOURCE in rickroll flag
do
  convert \
    grcon22_orig.png \
    -resize 600x \
    ${SOURCE}.png \
    -background white \
    -gravity north \
    -append \
    -extent 640x480 \
    -font Arial \
    -pointsize 24 \
    -draw "text 224,432 'VE3IRR/W3'" \
    grcon22_${SOURCE}.png
done

python3 ntsc_encode.py
