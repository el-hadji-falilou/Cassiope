#!/bin/bash

ulimit -t 10

set -e

: "${PROGNAME:=./minicipher}"
GROUP=$1

SEED=$(echo "$GROUP" | sha1sum | dd bs=1 count=32 2> /dev/null)

# Warning: N must be between 1 and 32
get_N_hexa_bytes () {
    if [ "$1" -ge 1 -a "$1" -le 32 ]; then
        RESULT=$(echo "$SEED 0" | md5sum | dd bs=1 count="$1" 2> /dev/null)
        SEED=$(echo "$SEED 1" | md5sum | dd bs=1 count=32 2> /dev/null)
    else
        echo "Please call get_N_hexa_bytes with an integer between 1 and 32."
        exit -1
    fi
}



if [ ! -x "$PROGNAME" ]; then
  echo "\"$PROGNAME\" is not a valid executable."
  exit -1
fi


echo "Checking basic encryption (a 16-bit word)" > response-encryption.0.txt
for i in $(seq 10); do
  get_N_hexa_bytes 20
  KEY=$RESULT
  get_N_hexa_bytes 4
  INPUT=$RESULT
  OUTPUT=$( printf "%s" "${INPUT}" | $PROGNAME -k "$KEY" 2>&1 )
  echo "$INPUT, $OUTPUT" >> response-encryption.0.txt
done


echo "Checking CBC encryption" >> response-encryption.0.txt
for i in 1 2 4 5 25 26 17 18 19 32; do
  get_N_hexa_bytes 20
  KEY=$RESULT
  get_N_hexa_bytes 4
  IV=$RESULT
  get_N_hexa_bytes $i
  INPUT=$RESULT
  OUTPUT=$( printf "%s" "${INPUT}" | $PROGNAME -M -i "$IV" -k "$KEY" 2>&1 )
  echo "$INPUT, $OUTPUT" >> response-encryption.0.txt
done

if diff -q <(grep -v '^$' response-encryption.0.txt) <(grep -v '^$' test-encryption.0.txt) > /dev/null 2>&1; then
    echo "SUCCESS"
    exit 0
else
    echo "FAILED"
    exit 1
fi
