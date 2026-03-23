CC=gcc
CFLAGS=-g -Wall -Wextra -std=c99
LDFLAGS=-lm
SRCS=main.c
BIN=main
OBJS=$(SRCS:.c=.o)

.PHONY: all clean

all: $(BIN)

$(BIN): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(FLAGS) -c -o $@ $^
clean: 
	rm $(BIN) $(OBJS) *.pam
