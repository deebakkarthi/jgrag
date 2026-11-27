#!/usr/bin/env python3
import os
import sys
import argparse

import html2text

PROGNAME = os.path.basename(sys.argv[0])


def main():
    parser = argparse.ArgumentParser()
    _ = parser.add_argument(
        "FILE",
        nargs="?",
        default="/dev/stdin",
        help="Defaults to STDIN",
        type=str,
    )
    _ = parser.add_argument(
        "-o",
        "--output",
        default="/dev/stdout",
        help="Defaults to STDOUT",
        type=str,
    )
    args = parser.parse_args()

    with open(args.FILE, "r") as f:
        html = f.read()
        with open(args.output, "w") as of:
            text_maker = html2text.HTML2Text()
            text_maker.ignore_emphasis = True
            text_maker.ignore_images = True
            text_maker.ignore_links = True
            # Don't bother with markdown it is ass anyway. Just output in
            # HTML
            text_maker.bypass_tables = True
            # Removes the HTML tags so that you end up with just the text
            # which is what we want
            text_maker.ignore_tables = True
            # Output ``` before and after <pre> blocks
            text_maker.backquote_code_style = True
            _ = of.write(text_maker.handle(html))
    return


if __name__ == "__main__":
    main()
