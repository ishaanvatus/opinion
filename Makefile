INCDIRS=-I.
CC=gcc
CFLAGS=-g -Wall -Wextra -std=c99
LDFLAGS=-lm
SRCS=main.c pam.c
BIN=main
OBJS=$(SRCS:.c=.o)

.PHONY: all clean sample

all: $(BIN)

$(BIN): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(FLAGS) -c -o $@ $^

clean: 
	rm -f $(BIN) $(OBJS) *.pam 1>/dev/null 2>&1
