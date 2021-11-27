"""
starts an Advent of Code 2021 day by copying from a template and requesting the input
"""

from argparse import ArgumentParser
from pathlib import Path
from typing import Optional

DEFAULT_TEMPLATE = Path("day00/")

def parse_args() -> tuple[Path, Path, Optional[str]]:
    parser = ArgumentParser(description = __doc__)
    parser.add_argument("day", type = Path,
        metavar = "DAY",
        help = "path of directory to create by copying from the template"
    )
    parser.add_argument("--template", type = Path, default = DEFAULT_TEMPLATE,
        metavar = "TEMPLATE",
        help = f"path of template for DAY, defaults to {DEFAULT_TEMPLATE}/",
    )
    cookie_group = parser.add_mutually_exclusive_group()
    cookie_group.add_argument("--raw", type = str,
        metavar = "COOKIE",
        help = "Advent of Code session cookie to request DAY's input with",
    )
    cookie_group.add_argument("--file", type = Path,
        metavar = "COOKIE",
        help = "path to file containing Advent of Code session cookie",
    )
    args = parser.parse_args()
    cookie = args.file.read_bytes() if args.file is not None else args.raw
    return args.template, args.day, cookie

def main(template: Path, day: Path, cookie: Optional[str] = None) -> None:
    raise NotImplementedError

if __name__ == "__main__":
    main(*parse_args())
