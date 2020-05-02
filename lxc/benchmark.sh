#!/bin/sh
for file in pts/*.pt; do
    # if [ "$file" != "pts/qg.order100.pt" ]; then
        output=$(./lxc -p -a1 -f < "$file")
        echo "$file,$output"
    # fi
done
