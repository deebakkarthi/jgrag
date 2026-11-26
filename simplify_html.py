#!/usr/bin/env python3
import sys
import os
import argparse
import bs4

PROGNAME = os.path.basename(sys.argv[0])


def main():
    parser = argparse.ArgumentParser(
        prog=PROGNAME,
        description="Remove extraneous elements from a HTML file",
    )
    parser.add_argument(
        "FILE",
        nargs="?",
        default="/dev/stdin",
        help="If FILE is not provided STDIN is read",
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "-i",
        "--inplace",
        action="store_true",
        help="Change inplace. Incompatible with -o and absent FILE",
    )
    output_group.add_argument(
        "-o", "--output", help="Defaults to STDOUT", default="/dev/stdout"
    )

    args = parser.parse_args()

    if args.FILE == "/dev/stdin" and args.inplace:
        print(f"{PROGNAME}: Cannot inplace change STDIN", file=sys.stderr)
        sys.exit(1)

    # If inplace output the input file
    # argparse performs the required checks, so this is safe.
    if args.inplace:
        args.output = args.FILE

    with open(args.FILE, "r") as f:
        html = f.read()

    soup = bs4.BeautifulSoup(markup=html, features="html.parser")

    tags_to_remove = ["head", "header", "footer"]

    for tag in tags_to_remove:
        for t in soup.find_all(tag):
            t.decompose()

    for elem in soup.find_all(id="cad_image_modal"):
        elem.decompose()

    for tag in soup.find_all(lambda x: x.has_attr("xmlns:html")):
        del tag["xmlns:html"]

    for tag in soup.find_all(True, style=True):
        del tag["style"]

    with open(args.output, "w") as f:
        f.write(soup.prettify())

    return


if __name__ == "__main__":
    main()
    sys.exit(0)
