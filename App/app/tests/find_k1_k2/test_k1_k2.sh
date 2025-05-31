#!/bin/bash

EXPECTED_1="7e99"
EXPECTED_2="14dc"

RESULT_1=$(python3 -c "
from find_key import find_k5_part1, find_k5_part2, find_k4_part1, find_k4_part2, find_k3_part1, find_k3_part2, find_k2, find_k1, init_inverse_ops
init_inverse_ops()
print(f'{find_k1():04x}')
")
RESULT_2=$(python3 -c "
from find_key import find_k5_part1, find_k5_part2, find_k4_part1, find_k4_part2, find_k3_part1, find_k3_part2, find_k2, init_inverse_ops
init_inverse_ops()
print(f'{find_k2():04x}')
")

if [[ "$RESULT_1" == "$EXPECTED_1" && "$RESULT_2" == "$EXPECTED_2" ]]; then
    echo 'SUCCESS'
else
    echo 'FAILED'
fi
