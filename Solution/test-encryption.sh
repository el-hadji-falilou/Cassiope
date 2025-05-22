#!/bin/sh

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

echo "Checking basic encryption (a 16-bit word)"
for i in $(seq 10); do
  get_N_hexa_bytes 20
  KEY=$RESULT
  get_N_hexa_bytes 4
  INPUT=$RESULT
  OUTPUT=$( printf "%s" "${INPUT}" | $PROGNAME -k "$KEY" 2>&1 )
  echo "  Test $i"
  echo "    Key = $KEY"
  echo "    Input = $INPUT"
  echo "    Command line = printf \"%s\" \"$INPUT\" | ./minicipher -k \"$KEY\" 2>&1"
  echo "    Output = $OUTPUT"
  echo
done
