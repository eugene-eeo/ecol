#!/bin/sh

cat ./class2_12.jsonl | xc/resmod 0 4 | xc/gc -u | xc/xc 1500 > class2_12.1.jsonl &
cat ./class2_12.jsonl | xc/resmod 1 4 | xc/gc -u | xc/xc 1500 > class2_12.2.jsonl &
cat ./class2_12.jsonl | xc/resmod 2 4 | xc/gc -u | xc/xc 1500 > class2_12.3.jsonl &
cat ./class2_12.jsonl | xc/resmod 3 4 | xc/gc -u | xc/xc 1500 > class2_12.4.jsonl &
wait
