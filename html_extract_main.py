#!/usr/bin/env python3
import os
import sys
import argparse

import bs4

PROGNAME = os.path.basename(sys.argv[0])


def extract_main(soup: bs4.BeautifulSoup):
    """
    Return only the main-header and the main-content
    """
    main_header = soup.find_all("div", id="main-header")
    main_content = soup.find_all("div", id="main-content")
    # These should always be singleton lists
    # But for the sake of completeness we're gonna iterate
    return "".join([str(s) for s in main_header]) + "".join(
        [str(s) for s in main_content]
    )


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
        soup = bs4.BeautifulSoup(html, "html.parser")
        with open(args.output, "w") as of:
            of.write(extract_main(soup))
    return


if __name__ == "__main__":
    main()
