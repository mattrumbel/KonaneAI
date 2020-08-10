#!bin/bash
for i in {0..10..1}
    do
        seconds = $SECONDS
        winner = python Konane.py
        difference = $((SECONDS - seconds))
        echo difference
    done