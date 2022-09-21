#!/usr/bin/env bash

qrencode -l H -s 2 -o flag.png "Sig. id. chal. 13: flag{sl0w_en0uGh_f0r_U}"
convert \
  ../ntsc/grcon22_orig.png \
  -resize 320x \
  flag.png \
  -background white \
  -gravity north \
  -append \
  -extent 320x256 \
  -font Arial \
  -pointsize 18 \
  -draw "text 106,232 'VE3IRR/W3'" \
  sstv.bmp

rm flag.png
