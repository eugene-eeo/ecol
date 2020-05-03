#!/bin/sh

for instance in 4-FullIns_4 5-FullIns_4 DSJC500.1 latin_square_10 \
                qg.order30 qg.order60 qg.order100 wap04a will199GPIA; do
    output=$(../lxc/lxc -p -f -a1 < "../lxc/pts/$instance.pt")
    echo "${instance},${output}"
done
