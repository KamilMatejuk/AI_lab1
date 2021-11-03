CC=g++

all: main

main: main.o puzzle.o solver.o utils.o
	$(CC) -o main main.o puzzle.o solver.o utils.o

%.o: %.cpp %.h
	$(CC) -c -o $@ $<

run:
	./main

.PHONY: clean
clean:
	rm -f main *.o *~
