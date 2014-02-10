#! python3

'''
A totally stupid and absolutely indispensable (python 3) script 
for converting source files to markdown documents

(C) 2014, Frederic Peschanski under the MIT License (cf. LICENSE)
'''


'''{
---
title:  'Markdownize documentation'
author:
- name: Frederic Peschanski
...
}'''




'''{

# Introduction #

The `markdownize` script allows to transform a source file
 written in any programming language into a markdown document.

This document is at the same time:
 - the reference manual for `markdownize` script
 - its commented source code
 - an example to `markdownize`

}'''

'''{

# Command line #

}'''

import argparse

# command line
cmd_parser = argparse.ArgumentParser()

cmd_parser.parse_args()

# conversion
