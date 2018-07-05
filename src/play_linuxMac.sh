#!/bin/bash

COUNT=1000
for a in $(seq 1 $COUNT); do
    python3 main.py --token <insert_token> --logic webjocke_custom
    sleep 2.0
done


wait
