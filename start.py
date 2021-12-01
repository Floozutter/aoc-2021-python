"""
starts an Advent of Code 2021 day by copying from a template and requesting the input
"""

import argparse
import shutil
import re
from pathlib import Path
from typing import Optional

DEFAULT_TEMPLATE = Path("day00/")
DEFAULT_INPUTFILE = Path("input.txt")

def request_aoc2021_input(day: int, cookie: str) -> str:
    import requests
    response = requests.get(
        f"https://adventofcode.com/2021/day/{day}/input",
        cookies = {"session": cookie},
    )
    return response.text

_PARSE_DAY_NUMBER_PATTERN = re.compile("[0-9]+")
def parse_day_number(day: str) -> int:
    matches = _PARSE_DAY_NUMBER_PATTERN.findall(day)
    if not matches:
        raise ValueError("no digit substring found")
    elif len(matches) == 1:
        return int(next(iter(matches)))
    else:
        raise ValueError("more than one digit substring found")

def parse_args() -> tuple[Path, Path, Path, Optional[str]]:
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("day", type = Path,
        metavar = "DAY",
        help = "path of directory to create by copying from the template",
    )
    parser.add_argument("--template", type = Path, default = DEFAULT_TEMPLATE,
        metavar = "TEMPLATE",
        help = f"path of template for DAY, defaults to {DEFAULT_TEMPLATE}/",
    )
    parser.add_argument("--inputfile", type = Path, default = DEFAULT_INPUTFILE,
        metavar = "INPUTFILE",
        help = f"path relative from TEMPLATE to write the requested input to",
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
    joined_inputfile = args.day / args.inputfile
    cookie = args.file.read_text().strip() if args.file is not None else args.raw
    return (
        args.day,
        args.template,
        joined_inputfile,
        cookie,
    )

def main(
    day: Path,
    template: Path,
    inputfile: Path,
    cookie: Optional[str] = None
) -> None:
    # copy the directory tree from template to day
    print(f"copying from {template}/ to {day}/...", end = "")
    try:
        shutil.copytree(template, day)
    except (shutil.Error, OSError) as err:
        print(f"!\nerror: {err}")
        return
    print(" done.")
    # write blank inputfile and exit if no cookie provided
    if cookie is None:
        print("no session cookie provided to request input with!")
        print(f"writing blank {inputfile}...", end = "")
        try:
            inputfile.touch()
        except OSError as err:
            print(f"!\nerror: {err}")
            return
        print(" done.")
        return
    print("session cookie provided to request input.")
    # parse day number from day path
    print(f"parsing day number from {day}/...", end = "")
    try:
        day_number = parse_day_number(day.name)
    except ValueError as err:
        print(f"!\nerror: {err}")
        return
    print(f" parsed as day {day_number}.")
    # request input for the parsed day number using cookie
    print(f"requesting input for day {day_number} using cookie...", end = "")
    try:
        inputtext = request_aoc2021_input(day_number, cookie)
    except ImportError as err:
        print(f"!\nerror: {err.name} not installed")
        return
    print(" done.")
    # write input to inputfile
    print(f"writing input to {inputfile}...", end = "")
    try:
        inputfile.write_text(inputtext)
    except OSError as err:
        print(f"!\nerror: {err}")
        return
    print(" done.")
    return

if __name__ == "__main__":
    main(*parse_args())
