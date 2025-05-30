#!/bin/bash

EXPECTED="0d0e"

RESULT=$(python3 -c "
from find_key import find_k5_part1, init_inverse_ops
init_inverse_ops()
print(f'{find_k5_part1():04x}')
")

if [ \"$RESULT\" == \"$EXPECTED\" ]; then
    echo 'SUCCESS'
else
    echo 'FAILED'
fi
