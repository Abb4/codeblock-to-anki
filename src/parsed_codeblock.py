from enum import Enum
from pathlib import Path

from typing import List

class CodeblockSeparator(Enum):
    BACKTICKS = 1

class ParsedCodeBlock:
    def __init__(self):
        self.completed: bool = False
        self.content: str = None
        self.start_pos: int = None
        self.end_pos: int = None
        self.separator: CodeblockSeparator = CodeblockSeparator.BACKTICKS
        self.file: Path = None
        self.type: str = None
        self.headers: List[str] = []

    def begin(self, start_pos: int, file: Path, type: str, headers: List[str]):
        self.start_pos = start_pos
        self.file = file
        self.type = type
        self.headers = headers

    def complete(self, content: str, end_pos: int):
        self.content = content
        self.end_pos = end_pos

        self.completed = True

    def is_completed(self) -> bool:
        return self.completed == True