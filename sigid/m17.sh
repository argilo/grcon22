#!/usr/bin/env bash

sox flag9.wav -r 8000 -t raw - | ~/git/m17-cxx-demod/build/apps/m17-mod -S VE3IRR -b > flag9.bin
