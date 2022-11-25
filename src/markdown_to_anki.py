from pathlib import Path

import genanki

from deck_assembler import DeckAssembler
from parsed_codeblock import ParsedCodeBlock
from codeblock_parser import CodeblockParser


def main():
    input = Path(".")
    output = Path(".")
    
    assembler = DeckAssembler()
    parser = CodeblockParser()
    
    codeblocks: ParsedCodeBlock = []
    
    files = list(input.glob("./**/*.md"))
     
    print(f"Checking {len(files)} files...") 
    
    for file in files:
        with file.open("r") as f:
            codeblocks.extend(
                parser.parse_text(f.read(), path=file) 
            )
            
    print(f"Found total {len(codeblocks)} codeblocks")
    
    codeblocks = list(filter(lambda c: c.type == "anki", codeblocks)) 
    
    print(f"Found 'anki' {len(codeblocks)} codeblocks")
    
    assembler.assemble_deck_from_codeblocks(codeblocks, output)
    
    decks = {}
    
    package_name = "deck_package.apkg" 
    
    package_path = output / package_name 
        
    genanki.Package(decks.values()).write_to_file(package_path.absolute())
    
    print(f"Created {package_path.absolute()}")

if __name__=="__main__":
    main()