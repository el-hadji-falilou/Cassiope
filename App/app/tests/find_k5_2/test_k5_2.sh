#!/bin/bash

EXPECTED="5080"

RESULT=$(python3 -c "
from find_key import find_k5_part2, init_inverse_ops
init_inverse_ops()
print(f'{find_k5_part2():04x}')
")

if [ \"$RESULT\" == \"$EXPECTED\" ]; then
    echo 'SUCCESS'
else
    echo 'FAILED'
fi
