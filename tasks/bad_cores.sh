#!/bin/sh
# Bad Cores for n = 5 .. 10 (to be ran locally)
python scripts/geng_raw.py --start=5 --end=11 | xc/gc -u | xc/xc 1500 > results/bad_cores_local.g6
