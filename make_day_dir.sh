#!/bin/bash

day=$1
name=$2

mkdir $day
cd $day
touch ${name}.py
touch ${name}_input.txt
touch ${name}_test_input.txt

echo "'''
Problem Notes
'''


def run_tests(filename):
    with open(filename, 'r') as f:
        pass


# testing
run_tests('${name}_test_input.txt')

# Actual work
# run_tests('${name}_input.txt')

" > ${name}.py

exit 0
