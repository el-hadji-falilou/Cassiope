#!/bin/bash

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


# Checking identity on 16-bit words
for i in $(seq 10); do
  get_N_hexa_bytes 20
  KEY=$RESULT
  get_N_hexa_bytes 4
  INPUT=$RESULT
  OUTPUT1=$( printf "%s" "${INPUT}" | $PROGNAME -k "$KEY" 2>&1 )
  OUTPUT2=$( printf "%s" "${OUTPUT1}" | $PROGNAME -d -k "$KEY" 2>&1 )
  if [ "$OUTPUT2" != "$INPUT" ]; then
    echo "FAILED"
    exit 1
  fi
done


# Checking identity in CBC mode using different lengths
for i in 1 2 4 5 25 26 17 18 19 32; do
  get_N_hexa_bytes 20
  KEY=$RESULT
  get_N_hexa_bytes 4
  IV=$RESULT
  get_N_hexa_bytes $i
  INPUT=$RESULT
  OUTPUT1=$( echo -n $INPUT | $PROGNAME -M -i "$IV" -k "$KEY" 2>&1 )
  OUTPUT2=$( echo -n $OUTPUT1 | $PROGNAME -d -M -i "$IV" -k "$KEY" 2>&1 )
  if [ "$OUTPUT2" != "$INPUT" ]; then
    echo "FAILED"
    exit 2
  fi
done


# Checking identity in CBC mode on random binary files
for i in 10 20 30 40 50 2048; do
  get_N_hexa_bytes 20
  KEY=$RESULT
  get_N_hexa_bytes 4
  IV=$RESULT
  TEMPFILE=$(mktemp tmpXXXXXXXXXXXXXXXXXXX)
  dd if=/dev/urandom of="$TEMPFILE" bs=512 count="$i" 2> /dev/null
  ID=$( cat $TEMPFILE | $PROGNAME -b -M -i "$IV" -k "$KEY" 2>&1 | $PROGNAME -b -d -M -i "$IV" -k "$KEY" 2>&1 | diff - $TEMPFILE)
  if [ "$ID" != "" ]; then
      echo "FAILED"
      exit 3
  fi
  rm -f $TEMPFILE
done

echo "SUCCESS"