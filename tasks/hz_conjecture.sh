#!/bin/sh
# Hilton Zhao for n = 5 .. 10 (to be ran locally)
python scripts/geng_raw.py --start=5 --end=11 | xc/gc -d2 -s | xc/xc 1500 > results/hz_conjecture_local.g6
