#!/usr/bin/env python

import re
import sys
import os

if len(sys.argv) != 2:
    print("Usage: {} <directory>".format(sys.argv[0]))
    sys.exit(1)

directory = sys.argv[1]

with open(os.path.join(directory, 'record.txt'), 'r') as infile:
    data = infile.read()

# Define a list of regular expressions and replacement strings
regex_patterns = [r'generate.*\n'
                  , r'reGenerate.*\n'
                  , r'frame:'
                  , r'time:'
                  , r'gen_time.*\n'
                  ]
replace_patterns = [''
                    ,''
                    ,''
                    ,''
                    ,'\n'
                    ]

# Iterate through the regex patterns and apply replacements
for regex, replacement in zip(regex_patterns, replace_patterns):
    data = re.sub(regex, replacement, data, count=0)

# Write the modified data back to the file
with open(os.path.join(directory, 'table.txt'), 'w') as outfile:
    outfile.write(data)

