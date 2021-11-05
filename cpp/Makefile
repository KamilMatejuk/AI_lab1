CC=g++

all: main

main: main.o puzzle.o solver.o utils.o heuristic.o
	$(CC) -o main main.o puzzle.o solver.o utils.o heuristic.o

%.o: %.cpp %.h
	$(CC) -c -o $@ $<

run:
	./main

push: clean
	git status
	git add ..
	git status
	git commit -m "commit"
	git push

.PHONY: clean
clean:
	rm -f main *.o *~
