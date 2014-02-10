    #! python3
    
**Markdownize**: a totally stupid and absolutely indispensable (python 3) script 
for converting source files to markdown documents

(C) 2014, Frederic Peschanski under the MIT License (cf. LICENSE)
    
    import sys
    

# Introduction #

The `markdownize` script allows to transform a source file
 written in any programming language into a markdown document.

This document is at the same time:
 - the reference manual for `markdownize` script
 - its commented source code
 - an example to `markdownize`

    

# Command line #

    
    import argparse
    
    # command line
    cmd_parser = argparse.ArgumentParser()
    
    
The `--input` (or `-i`) option of the command line is the input file to markdownize.
If left unspecified the input will be from the standard input.
    
    cmd_parser.add_argument('-i', '--input', dest='input',
                            type=argparse.FileType('r'), default=sys.stdin,
                            help="The input file to markdownize.")
    
The `--begin` (or `-b`) and `--end` (or `-e`) optional arguments allow to select the delimiters between
 the document blocks and the source code blocks.

By default, the C-compatible block comments `/*{` for begin, and `}*/` for end are set.

This means that a document block will be of the form:

    /*{

      ... Contents of the document ...

    }*/

while everything else will be considered a source code block.

    
    cmd_parser.add_argument('-b', '--begin', dest='begin', default=r'/*{', 
                            help="the delimiter to begin a document block.")
    
    cmd_parser.add_argument('-e', '--end', dest='end', default=r'}*/',
                            help="the delimiter to end a document block.")
    
The `--output` (or `-o`) option is used to specify the output file. By default, this is the standard output.
    
    cmd_parser.add_argument('-o', '--output', dest='output',
                            type=argparse.FileType('w'), default=sys.stdout,
                            help="the output file to generate.")
    

And now the command line parsing begins.

    
    class CmdArgs:
        pass
    
    cmd_args = CmdArgs()
    
    cmd_parser.parse_args(namespace=cmd_args)
    
_Remark_: we adopt in this script a "fail first" philosophy that
aborpts the conversion as soon as an error is encountered.
    
    def abort(msg):
        print("""Error: {}
        ==> Cannot markdownize ... abort :-(
        """.format(msg), file=sys.stderr)
        sys.exit(1)
    

# Conversion #

The conversion is performed by a `Markdownizer`.

    
    def markdownize(input_file, output_file, begin_doc, end_doc):
    
This is the core of the transformation.
    
        in_document = False
        dedent_value = 0
    
        line_count = 0
    
        try:
            for line in input_file:
                line_count += 1
                #print("line #{} = ".format(line_count),line,file=sys.stderr)
    
                #if line_count == 124:
                #    import pdb; pdb.set_trace()
    
                if not in_document:
    
If we are not in a document block, then we first
try to find a begin delimiter block.
    
                    if line.lstrip().rstrip() == begin_doc:
                        in_document = True
                        dedent_value = 0
                        while line[dedent_value].isspace():
                            dedent_value += 1
                    else:
    
Otherwise, we are in a code block so we have to insert exactly
four spaces to produce a valid markdown document.
    
                        try:
                            output_file.write('    ' + line)
                        except:
                            abort("problem while writing output file at line {}".format(line_count))
                else:
    
If we are in a document block, then we first try
to find an end delimiter block.
    
                    if line.lstrip().rstrip() == end_doc:
                        in_document = False
                        dedent_value = 0
                    else:
    
Otherwise, we are still in a document block so we dedent
some prepending spaces (in a fairly robust way) and
then copy the line almost "as it is".
    
                        out_line = line[:]
                        for i in range(min(dedent_value, len(out_line))):
                            if out_line[0] == ' ':
                                out_line = out_line[1:]
                        try:
                            output_file.write(out_line)
                        except:
                            abort("problem while writing output file at line {}".format(line_count))
    
        except:
            abort("problem while reading input file at line {}".format(line_count))
                          
        input_file.close()
        output_file.close()
                  
    

The main conversion starts now.

    
    markdownize(cmd_args.input, cmd_args.output, cmd_args.begin, cmd_args.end)
    

And if all went OK then we have a nice markdown produced.

# Conclusion #

That's all folks !

