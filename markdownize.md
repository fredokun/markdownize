```python
#! python3

```

**Markdownize**: a totally stupid and absolutely indispensable (python 3) script 
for converting source files to markdown documents

(C) 2014-2018, Frederic Peschanski under the MIT License (cf. LICENSE)


```python
import sys
import re

```


# Introduction #

The `markdownize` script allows to transform a source file
 written in any programming language into a markdown document.

This document is at the same time:
 - the reference manual for `markdownize` script
 - its commented source code
 - an example to `markdownize`





# Command line #



```python
import argparse

# command line
cmd_parser = argparse.ArgumentParser()


```

The `--input` (or `-i`) option of the command line is the input file to markdownize.
If left unspecified the input will be from the standard input.


```python
cmd_parser.add_argument('-i', '--input', dest='input',
                        type=argparse.FileType('r'), default=sys.stdin,
                        help="The input file to markdownize.")

```

The `--output` (or `-o`) option is used to specify the output file. By default, this is the standard output.


```python
cmd_parser.add_argument('-o', '--output', dest='output',
                        type=argparse.FileType('w'), default=sys.stdout,
                        help="the output file to generate.")

```

The `--begin` (or `-b`) and `--end` (or `-e`) optional arguments allow to select the delimiters between
 the document blocks and the source code blocks.

By default, the C-compatible block comments `/*{` for begin, and `}*/` for end are set.

This means that a document block will be of the form:

    /*{

      ... Contents of the document ...

    }*/

while everything else will be considered a source code block.



```python
cmd_parser.add_argument('-b', '--begin', dest='begin', default=r'/*{', 
                        help="the delimiter to begin a document block.")

cmd_parser.add_argument('-e', '--end', dest='end', default=r'}*/',
                        help="the delimiter to end a document block.")

```

The option `--remove-prefix` (or `-rp`) will remove any occurrence of the specified
 *prefix* inside each document block (as delimited by the `--begin` and `--end` options).

For example if the prefix is `";; "` then if a line within a document block is so prefixed,
 e.g. `";; this is *inside* a document block"`  then it will be rewritten as
`"this is *inside* a document block"`. Otherwise the line is left unchanged.

This option is useful for programming languages having no support for block comments.
By default, there is no prefix specified (i.e. it is the empty string `""`).


```python
cmd_parser.add_argument('-rp', '--remove-prefix', dest='prefix', default="",
                        help="the prefix to remove in a document block.")

```

Markdownize supports variants of the previous options with a `-re` suffix that allows to
use regular expressions instead of simple string: 

 - `--begin-re <regex>`  the begin document block as a regular expression
 - `--close-re <regex>`  the end document block as a regular expression
 - `--remove-prefix-re <regex>` the remove prefix as a regular expression

Because these options are for relatively advanced usage, there is no short version provided.



```python
cmd_parser.add_argument('--begin-re', dest='begin_re', default=None, 
                        help="the delimiter to begin a document block (as a regular expression).")

cmd_parser.add_argument('--end-re', dest='end_re', default=None,
                        help="the delimiter to end a document block (as a regular expression).")

cmd_parser.add_argument('--remove-prefix-re', dest='prefix_re', default=None,
                        help="the prefix to remove in a document block (as a regular expression).")


```

The option `--lang` (or `-l`) allows to specify a language for the
code blocks. This is supported in e.g. github markdown and also
pandoc.


```python
cmd_parser.add_argument('-l', '--lang', dest='lang', default=None, 
                        help="the language specifier for code blocks.")


```


And now the command line parsing begins.



```python
class CmdArgs:
    pass

cmd_args = CmdArgs()

cmd_parser.parse_args(namespace=cmd_args)

```

_Remark_: we adopt in this script a "fail first" philosophy that
aborpts the conversion as soon as an error is encountered.


```python
def abort(msg):
    print("""Error: {}
    ==> Cannot markdownize ... abort :-(
    """.format(msg), file=sys.stderr)
    sys.exit(1)

```


# Conversion #

First we need a simple auxiliary function that tests if some
provided text is recognized by a document *marker* (begin, end
 or remove prefix). It returns the recognized (sub-)string or
 None if there is no match.


```python
REGULAR_EXPRESSION_TYPE = re.compile('').__class__

def recognize(text, marker, start_only=False):
    if isinstance(marker, str):
        if start_only:
            if text.startswith(marker):
                return marker
            else:
                return None
        else:
            if text == marker:
                return marker
            else:
                return None
    elif isinstance(marker, REGULAR_EXPRESSION_TYPE):
        if start_only:
            match_obj = marker.match(text)
            if match_obj is None:
                return None
            else:
                return match_obj.group(0)
        else:
            match_obj = marker.fullmatch(text)
            if match_obj is None:
                return None
            else:
                return match_obj.group(0)
    else:
        raise ValueError("Cannot recognize this marker: {}".format(marker))

```


The conversion is performed by the following function.



```python
def markdownize(input_file, output_file, begin_doc, end_doc, remove_prefix, lang):

```

This is the core of the transformation.


```python
    in_document = False
    code_block_started = False
    dedent_value = 0

    line_count = 0

    try:
        for line in input_file:
            line_count += 1
            #print("line #{} = ".format(line_count),line,file=sys.stderr)

            #if line_count == 124:
            #    import pdb; pdb.set_trace()

            if not in_document:

```

If we are not in a document block, then we first
try to find a begin delimiter block.


```python
                if recognize(line.lstrip().rstrip(), begin_doc) is not None:
                    in_document = True
                    dedent_value = 0
                    while line[dedent_value].isspace():
                        dedent_value += 1

```

We have to close the code block if it is started.

```python
                    if code_block_started:
                        if lang is None:
                            output_file.write('\n')
                        else:
                            output_file.write('```\n')

                        code_block_started = False

```

And we put a newline instead of the begin block.

```python
                    output_file.write('\n')

                else:

```

Otherwise, we are in a code block. If it is not yet started
then we start it, except if the current line is blank.


```python
                    if line != '\n' and not code_block_started:
                        if lang is None:
```

We add a blank line if no language is set.

```python
                            output_file.write('\n')
                        else:
```

Otherwise we put the code block header.

```python
                            output_file.write('```{}\n'.format(lang))

                        code_block_started = True

                    if lang is None:

```

If the language for code blocks is not set, we just insert exactly
four spaces to produce a valid markdown document.


```python
                        output_file.write('    ' + line)
                    else:

```

Otherwise, we simply copy the input line as it is.


```python
                        output_file.write(line)
            else:

```

If we are in a document block, then we first try
to find an end delimiter block.


```python
                if recognize(line.lstrip().rstrip(), end_doc) is not None:
                    in_document = False
                    dedent_value = 0

```

And we put a newline instead of the end block.

```python
                    output_file.write('\n')

                else:

```

Otherwise, we are still in a document block.


```python
                    out_line = line[:]

```

First, we dedent
some prepending spaces (in a fairly robust way) and
then copy the line almost "as it is".

```python
                    for i in range(min(dedent_value, len(out_line))):
                        if out_line[0] == ' ':
                            out_line = out_line[1:]

                    if remove_prefix:
```

Then, if there is a prefix to remove (`--remove-prefix` option), then
we first check if the line read starts with the specified prefix.
and if so the prefix is removed.

```python
                        removed_text = recognize(out_line, remove_prefix, start_only=True)
                        if removed_text is not None:
                            out_line = out_line[len(removed_text):]

                    output_file.write(out_line)

    except Exception as e:
        abort("problem while markdownizing at line {}\n ==> cause: {}".format(line_count, e))

```

If at the end we were in a code block, then we have to close it.

```python
    if code_block_started:
        if lang is None:
            output_file.write('\n')
        else:
            output_file.write('```\n')
        code_block_started = False # Remember the boy scout rule ...

    input_file.close()
    output_file.close()

```

If regular expressions are provided, then we compile them.


```python
doc_begin = cmd_args.begin
if cmd_args.begin_re:
    doc_begin = re.compile(cmd_args.begin_re)

doc_end = cmd_args.end
if cmd_args.end_re:
    doc_end = re.compile(cmd_args.end_re)

doc_prefix = cmd_args.prefix
if cmd_args.prefix_re:
    doc_prefix = re.compile(cmd_args.prefix_re)

```

Thus in the conversion we will have to make a clear distinction between
 strings or compiled regexps when handling these parameters.

```python
    
```

The main conversion starts now.



```python
markdownize(cmd_args.input, cmd_args.output, doc_begin, doc_end, doc_prefix, cmd_args.lang)

```

And if all went OK then we have a nice markdown produced.

# Conclusion #

That's all folks !

