#!/usr/bin/env bash

set -e

qrencode -o rickroll.png 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
qrencode -o flag.png 'FLAG{2OBGfE29cR1SpOXuJpI832FyAWvNPLtC}'

convert \
  grcon22_orig.png \
  -resize 600x \
  rickroll.png \
  -background white \
  -gravity north \
  -append \
  -extent 640x480 \
  -font Arial \
  -pointsize 24 \
  -draw "text 224,432 'VE3IRR/W3'" \
  grcon22_rickroll.png

convert \
  grcon22_orig.png \
  -resize 600x \
  flag.png \
  -background white \
  -gravity north \
  -append \
  -extent 640x480 \
  -font Arial \
  -pointsize 24 \
  -draw "text 224,432 'VE3IRR/W3'" \
  grcon22_flag.png

python3 ntsc_encode.py
