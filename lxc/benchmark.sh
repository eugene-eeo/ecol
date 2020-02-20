#!/bin/sh
for file in pts/*.pt; do
    if [ "$file" != "pts/latin_square_10.pt" ] && [ "$file" != "pts/qg.order100.pt" ]; then
        output=$(./lxc -p -a10 < "$file")
        echo "$file,$output"
    fi
done
