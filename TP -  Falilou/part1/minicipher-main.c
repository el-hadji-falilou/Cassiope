/***********************************************************
 * main-1.c : skeleton file for the command line interface *
 ***********************************************************/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "minicipher.h"


/***********************
 * Command Line Handle *
 ***********************/


/* Argument declaration with default values */
/********************************************/

// By default, the program's action is to encrypt
enum {d_encrypt, d_decrypt} direction = d_encrypt;

// Default mode of operation (how we read and write values)
enum {hexa, binary} encoding = hexa;

// The default key is the null key
int keys[5] = {0, 0, 0, 0, 0};

// minicipher can work with only one block (in which case the program
// only reads 2 bytes) or in CBC mode with padding (which means it can
// handle an arbitrary input)
enum {monobloc, CBC_wpadding} mode = monobloc;

// The IV value is required with CBC mode
int iv = 0;

// EOF signal for the CBC mode
int eof = 0;



void usage (const char* const progname, const char* const msg) {
  if (msg != 0) 
    fprintf (stderr, "%s\n\n", msg);
  fprintf (stderr, "Usage: %s [-e|-d] [-b] [-1|-M] [-k <key>] [-i <iv>]\n\n", progname);
  fprintf (stderr, "  -e       encryption mode (defaut)\n");
  fprintf (stderr, "  -d       decryption mode\n");
  fprintf (stderr, "  -1       only one block will be en/de-crypted (defaut)\n");
  fprintf (stderr, "  -b       input and output are considered as binary streams (and not hexadecimal strings)\n");
  fprintf (stderr, "  -M       CBC mode, which allows the input to be arbitrary\n");
  fprintf (stderr, "  -k <key> key definition (80 bits, or 20 hexa chars)\n");
  fprintf (stderr, "           (by defaut, the null key is used)\n");
  fprintf (stderr, "  -i <iv>  IV (initial value), used in the CBC mode (16 bits, or 4 hexa chars)\n\n");
  fprintf (stderr, "           (the default value is a null IV)\n");

  exit (1);
}


static inline int _4b_from_hexa (char c) {
  if (c >= '0' && c <= '9')
    return (c - '0');
  if (c >= 'A' && c <= 'F')
    return ((c - 'A') + 10);
  if (c >= 'a' && c <= 'f')
    return ((c - 'a') + 10);
  return 0xff;
}


int read_value (const char* arg, int nWords, int* res) {
  int i, j, c;

  if ((int) strlen (arg) != (nWords * 4))
    return 0;

  for (i=0; i<nWords; i++) {
    res[i] = 0;
    for (j=0; j<4; j++) {
      c = _4b_from_hexa (arg[4*i + j]);
      if (c == 0xff)
	return 0;
      res[i] <<= 4;
      res[i] |= c;
    }
  }

  return 1;
}


void get_opts (int argc, char** argv) {
  int i;
  char* argument;

  for (i=1; i<argc; i++) {
    if (argv[i][0] != '-')
      usage (argv[0], "Invalid argument: should start with a dash (-).");
    switch (argv[i][1]) {
    case 'e':
      direction = d_encrypt;
      goto check_end_of_arg;
    case 'd':
      direction = d_decrypt;
      goto check_end_of_arg;
    case '1':
      mode=monobloc;
      goto check_end_of_arg;
    case 'M':
      mode=CBC_wpadding;
      goto check_end_of_arg;
    case 'b':
      encoding=binary;
      goto check_end_of_arg;

    check_end_of_arg:
      if (argv[i][2] != 0)
	usage (argv[0], "The argument should not be followed by a parameter.");
      break;

    case 'k':
      if (argv[i][2] == 0) {
	if (argv[i+1] == 0)
	  usage (argv[0], "'-k' must be followed by a 20-char key.");
	argument = argv[++i];
      } else
	argument = &(argv[i][2]);
      if (! read_value (argument, 5, keys))
	usage (argv[0], "Invalid key.");
      break;
      
    case 'i':
      if (argv[i][2] == 0) {
	if (argv[i+1] == 0)
	  usage (argv[0], "'-i' must be followed by a 4-char key.");
	argument = argv[++i];
      } else
	argument = &(argv[i][2]);
      if (! read_value (argument, 1, &iv))
	usage (argv[0], "Invalid IV.");
      break;
      
    default:
      usage (argv[0], "Unknown option..");
    }
  }
}


int get_16b_from_stdin (int padding) {
  unsigned char input[5];
  int nextchar;
  int res, i;

  if (encoding == hexa) {
    for (i = 0; i<4; i++) {
      nextchar = getchar();
      if (nextchar >= 0)
        input[i] = (char) nextchar;
      else
        input[i] = 0xff;
      if (_4b_from_hexa (input[i]) == 0xff)	
	{
	  if (padding) {
	    eof = 1;
	    input[i] = '8';
	    for (i++; i<4; i++)
	      input[i] = '0';
	    break;
	  } else
	    return -1;
	}
    }
    input[4]=0;
    
    if (! read_value ((const char*) input, 1, &res)) {
      if (padding) {
	eof = 1;
	return 0x8000;
      } else
	return -1;
    }

    return res;

  } else {

    // encoding == binary
    for (i = 0; i<2; i++) {
      nextchar = getchar();
      if (nextchar != EOF) {
        input[i] = (char) nextchar;
      } else {
	if (padding) {
	  eof=1;
	  input[i] = (char) 0x80;
	  input[i+1] = 0;
	  break;
	} else
	  return -1;
      }
    }
    return ((input[0] << 8) | input[1]);
  }
}

void print_16b (int output) {
  if (encoding == hexa) {
    printf ("%4.4x", output);
  } else {
    // encoding == binary
    putchar (output >> 8);
    putchar (output & 0xff);
  }
}
  
void print_16b_and_truncate (int output) {
  if (encoding == hexa) {
    if (output == 0x8000)
      return;
    if ((output & 0x0fff) == 0x800) {
      printf ("%1.1x", output >> 12);
      return;
    }
    if ((output & 0x00ff) == 0x80) {
      printf ("%2.2x", output >> 8);
      return;
    }
    if ((output & 0x000f) == 0x8) {
      printf ("%3.3x", output >> 4);
      return;
    }
    fprintf (stderr, "Padding Error: the final pattern could not be found.");

  } else {
    // encoding == binary
    if (output == 0x8000)
      return;
    if ((output & 0x00ff) == 0x80) {
      putchar (output >> 8);
      return;
    }
    fprintf (stderr, "Padding Error: the final pattern could not be found.");
  }
}

int main (int argc, char** argv) {
  int input;
  int output;

  init_inverse_ops();

  get_opts (argc, argv);

  switch (mode) {
  case monobloc:
    
    input = get_16b_from_stdin (0);
    if (input == -1)
      usage (argv[0], "Unexpected char: the input was supposed to be hexadecimal chars.");

    switch (direction) {
    case d_encrypt:
      output = minicipher_encrypt (input, keys);
      break;
    case d_decrypt:
      output = minicipher_decrypt (input, keys);
      break;
    }

    print_16b (output);
    break;

  case CBC_wpadding:
    switch (direction) {
    case d_encrypt:
      while (!eof) {
	input = get_16b_from_stdin (1);
	output = minicipher_encrypt (input ^ iv, keys);
	iv = output ^ input;
	print_16b (output);
      }
      break;

    case d_decrypt:
      input = get_16b_from_stdin (0);
      while (input != -1) {
	output = minicipher_decrypt (input, keys) ^ iv;
	iv = input ^ output;
	input = get_16b_from_stdin (0);
	if (input != -1)
	  print_16b (output);
	else
	  print_16b_and_truncate (output);
      }
      break;
    }
  }

  if (encoding == hexa)
    printf ("\n");
  exit (0);
}
