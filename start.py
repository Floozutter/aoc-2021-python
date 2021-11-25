"""
starts an Advent of Code 2021 day by copying from the day00/ template and requesting the input
"""

import argparse
from typing import Optional

def parse_args() -> tuple[str, Optional[str]]:
    raise NotImplementedError

def main(daystr: str, cookie: Optional[str] = None) -> None:
    raise NotImplementedError

if __name__ == "__main__":
    main(*parse_args())
