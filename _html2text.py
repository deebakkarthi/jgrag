#!/usr/bin/env python3
import os
import sys
import argparse

from resiliparse.extract.html2text import extract_plain_text

PROGNAME = os.path.basename(sys.argv[0])


def html2text(html: str):
    return extract_plain_text(
        html,
        main_content=True,
        preserve_formatting=False,
        alt_texts=False,
        list_bullets=False,
        comments=False,
        form_fields=False,
        post_meta=False,
    )


def main():
    parser = argparse.ArgumentParser()
    _ = parser.add_argument(
        "FILE",
        nargs="?",
        help="HTML file to convert. Defaults to STDIN",
        default="/dev/stdin",
        type=str,
    )
    _ = parser.add_argument(
        "-o",
        "--output",
        required=False,
        help="FILE to write the output. Defaults to STDOUT",
        default="/dev/stdout",
        type=str,
    )

    args = parser.parse_args()

    with open(args.FILE, "r") as f:
        html = f.read()
        with open(args.output, "w") as ofile:
            _ = ofile.write(html2text(html))
    return


if __name__ == "__main__":
    main()
