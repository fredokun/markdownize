Markdownize
===========

A totally stupid and absolutely indispensable (python 3) script 
for converting source files to markdown documents

## Usage

    markdownize.py [-h] [-i INPUT] [-o OUTPUT] [-b BEGIN] [-e END]
                        [-l LANG]


    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                            The input file to markdownize.
      -o OUTPUT, --output OUTPUT
                            the output file to generate.
      -b BEGIN, --begin BEGIN
                            the delimiter to begin a document block.
      -e END, --end END     the delimiter to end a document block.
      -l LANG, --lang LANG  the language specifier for code blocks.


## Example

    python3 ./markdownize.py --input ./markdownize.py --output ./markdownize.md --begin "'''{" --end "}'''"
