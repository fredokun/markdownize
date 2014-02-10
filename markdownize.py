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


'''{
The main argument of the command line is the input file to markdownize.
}'''

cmd_parser.add_argument('input', type=argparse.FileType('r'),
                        help="The input file to markdownize.")

'''{
The `--begin` (or `-b`) and `--end` (or `-e`) optional arguments allow to select the delimiters between
 the document blocks and the source code blocks.

By default, the C-compatible block comments `/*{` for begin, and `}*/` for end are set.

This means that a document block will be of the form:

    /*{

      ... Contents of the document ...

    }*/

while everything else will be considered a source code block.

}'''

cmd_parser.add_argument('-b', '--begin', dest='begin', default=r'/*{', 
                        help="the delimiter to begin a document block.")

cmd_parser.add_argument('-e', '--end', dest='end', default=r'}*/',
                        help="the delimiter to end a document block.")

'''{
The `--output` (or `-o`) option is used to specify the output file. By default, this is the input file
 with the suffix `.md` appended.
}'''

cmd_parser.add_argument('-o', '--output',
                        help="the output file to generate.")


'''{

And now the command line parsing begins.

}'''

class CmdArgs:
    pass

cmd_args = CmdArgs()

cmd_parser.parse_args(namespace=cmd_args)

'''{

Let's specify the output file, and defaults to the `.md` suffix.

}'''

if not cmd_args.output:
    cmd_args.output = str(cmd_args.input) + ".md"

'''{
_Remark_: we adopt in this script a "fail first" philosophy that
aborpts the conversion as soon as an error is encountered.
}'''

import sys

def abort(msg):
    print("""Error: {}
    ==> Cannot markdownize ... abort :-(
    """.format(msg), file=sys.stderr)
    sys.exit(1)

'''{

# Conversion #

The conversion is performed by a `Markdownizer`.

}'''

import re

def markdownize(input_file, output_filename, begin_doc, end_doc):
    '''{
    This is the core of the transformation.
    }'''

    try:
        output_file = open(output_filename, 'w')
    except:
        abort("cannot open output file for writing: {}".format(output_filename))

    in_document = False
    dedent_value = 0
    
    try:
        for line in input_file:
            if not in_document:
                '''{
                If we are not in a document block, then we first
                try to find a begin delimiter block.
                }'''
                m = re.match(r"^([ \t]*)" + begin_doc + r"[ \t]*$")
                if m:
                    in_document = True
                    dedent_value = len(m.group[1]) if m.group[1] else 0
                else:
                    '''{
                    Otherwise, we are in a code block so we have to insert exactly
                    four spaces to produce a valid markdown document.
                    }'''
                    try:
                        output_file.write('    ' + line)
                    except:
                        abort("problem while writing output file")
            else:
                '''{
                If we are in a document block, then we first try
                to find an end delimiter block.
                }'''
                m = re.match(r"^([ \t]*)" + end_doc + r"[ \t]*$")
                if m:
                    in_document = False
                    dedent_value = 0
                else:
                    '''{
                    Otherwise, we are still in a document block so we dedent
                    some prepending spaces (in a fairly robust way) and
                    then copy the line almost "as it is".
                    }'''
                    out_line = line[:]
                    for i in range(dedent_value):
                        if out_line[i] == ' ':
                            out_line = out_line[1:]
                    try:
                        output_file.write(out_line)
                    except:
                        abort("problem while writing output file")

    except:
        abort("problem while reading input file")
                      
    input_file.close()
    output_file.close()
              

'''{

The main conversion starts now.

}'''

markdownize(cmd_args.input, cmd_args.output, cmd_args.begin, cmd_args.end)

'''{

And if all went OK then we have a nice markdown produced.

# Conclusion #

That's all folks !

}'''


