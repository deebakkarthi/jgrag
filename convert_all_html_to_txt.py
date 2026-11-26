#!/usr/bin/env python3
import glob
from pathlib import Path

from _html2text import html2text


def main():
    p = Path(".")
    for path in list(p.glob("documents/html/*/*.html")):
        with open(path, "r") as f:
            html = f.read()
            output_file = Path(
                path.parts[0],
                "txt",
                *path.parts[2:-1],
                path.parts[-1].replace("html", "txt")
            )
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(html2text(html))
    return


if __name__ == "__main__":
    main()
