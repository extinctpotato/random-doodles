#!/bin/bash

sleep 1 && echo 'Slept 1' &
sleep 2 && echo 'Slept 2' &
sleep 3 && echo 'Slept 3' &

wait
