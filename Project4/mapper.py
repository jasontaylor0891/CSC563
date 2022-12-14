#!/usr/bin/env python
import sys
import re
 
#--- get all lines from stdin ---
for line in sys.stdin:
    
    #--- remove leading and trailing whitespace---
    line = line.strip()
    
    #--- remove special characters---
    line_wo = re.sub(r"[^a-zA-Z]", " ",line)

    #--- split the line into words ---
    words = line_wo.split()

    #--- output tuples [word, 1] in tab-delimited format---
    for word in words: 
        print '%s\t%s' % (word, "1")
