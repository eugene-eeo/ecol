#!/bin/sh
for file in pts/*.pt; do
    if [ "$file" != "pts/latin_square_10.pt" ]; then
        output=$(cat "$file" | ./lxc -p -a10)
        echo "$file,$output"
    fi
done
