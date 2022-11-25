from pathlib import Path

class ParsedCallout:
    def __init__(self):
        self.completed: bool = False
        self.content: str = None
        self.start_pos: int = None
        self.end_pos: int = None
        self.file: Path = None
        self.type: str = None
        self.attributes: list[str] = []

    def begin(self, start_pos: int, file: Path, type: str, attributes: list[str]):
        self.start_pos = start_pos
        self.file = file
        self.type = type
        self.attributes = attributes
    
    def complete(self, content: str, end_pos: int):
        self.content = content
        self.end_pos = end_pos
        
        self.completed = True
    
    def is_completed(self) -> bool:
        return self.completed == True