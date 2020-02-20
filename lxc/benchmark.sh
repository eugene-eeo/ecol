#!/bin/sh
for file in pts/*.pt; do
    output=$(./lxc -p -a20 < "$file")
    echo "$file,$output"
done
