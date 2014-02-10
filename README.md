Markdownize
===========

A totally stupid and absolutely indispensable (python 3) script 
for converting source files to markdown documents

## usage ## 

    markdownize.py [-h] [-i INPUT] [-b BEGIN] [-e END] [-o OUTPUT]

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                            The input file to markdownize.
      -b BEGIN, --begin BEGIN
                            the delimiter to begin a document block.
      -e END, --end END     the delimiter to end a document block.
      -o OUTPUT, --output OUTPUT
                            the output file to generate.


## Example ##

    python3 ./markdownize.py --input ./markdownize.py --output ./markdownize.md --begin "'''{" --end "}'''"
