#!/bin/bash

EXPECTED="14dc"

RESULT=$(python3 -c "
from find_key import find_k5_part1, find_k5_part2, find_k4_part1, find_k4_part2, find_k3_part1, find_k3_part2, find_k2, init_inverse_ops
init_inverse_ops()
print(f'{find_k2():04x}')
")

if [ \"$RESULT\" == \"$EXPECTED\" ]; then
    echo 'SUCCESS'
else
    echo 'FAILED'
fi
