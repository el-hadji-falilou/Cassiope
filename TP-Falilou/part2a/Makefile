# Part 2a Makefile

CFLAGS=-Wall -Wextra -Werror -Wcast-qual -Wconversion -Wsign-conversion
CC=gcc

PHONY=default clean python c

default:
	@echo "Please choose whether you want to use C or Python"
	@echo "To this end, please type make c or make python"

c: compute-probas
	./compute-probas

python: compute-probas.py
	./compute-probas.py


clean:
	rm -f *.o *.pyc compute-probas
