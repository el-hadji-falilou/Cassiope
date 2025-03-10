# Part 1 Makefile

CFLAGS=-Wall -Wextra -Werror -Wcast-qual -Wconversion -Wsign-conversion
CC=gcc

PHONY=default clean python c

default:
	@echo "Please choose whether you want to use C or Python"
	@echo "To this end, please type make c or make python"

c: minicipher-c
	rm -f minicipher
	ln -s minicipher-c minicipher

python: minicipher-main.py minicipher.py
	rm -f minicipher
	ln -s minicipher-main.py minicipher
	chmod +x minicipher



minicipher-c: main-1.o minicipher.o
	gcc -o $@ $+

main-1.o: main-1.c minicipher.h




clean:
	rm -f *.o *.pyc minicipher minicipher-c
