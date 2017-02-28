# Makefile for testing

SOURCES=$(shell ls test/*.c)
TARGETS=$(subst test/, test/gen/, $(SOURCES))

all: $(TARGETS)

test/gen/%.c : test/%.c
	python3 emplc.py $< | indent > $@

clean:
	rm test/gen/*
