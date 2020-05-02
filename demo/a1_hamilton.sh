#!/bin/sh


echo "Number of graphs of size 9:"
geng -qc 9 | wc -l

echo
echo "Split:"
geng -qc 9 0/4 | wc -l
geng -qc 9 1/4 | wc -l
geng -qc 9 2/4 | wc -l
geng -qc 9 3/4 | wc -l
