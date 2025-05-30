#!/bin/bash

EXPECTED_1="5415"
EXPECTED_2="82aa"

RESULT_1=$(python3 -c "
from find_key import find_k5_part1, find_k5_part2, find_k4_part1, init_inverse_ops
init_inverse_ops()
print(f'{find_k4_part1():04x}')
")
RESULT_2=$(python3 -c "
from find_key import find_k5_part1, find_k5_part2, find_k4_part2, init_inverse_ops
init_inverse_ops()
print(f'{find_k4_part2():04x}')
")

if [[ "$RESULT_1" == "$EXPECTED_1" && "$RESULT_2" == "$EXPECTED_2" ]]; then
    echo 'SUCCESS'
else
    echo 'FAILED'
fi
