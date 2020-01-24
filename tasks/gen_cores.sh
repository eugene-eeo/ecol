#!/bin/sh
geng="$HOME/Downloads/nauty26r12/geng"
for i in $(seq 2 20); do
    # Generate cores such that they have delta = 2 (strictly)
    # and have a cycle (otherwise guaranteed class 1)
    "$geng" -D2 -q "$i" | xc/gc -D2 -c
done
