from pathlib import Path

import genanki
from callout_parser import CalloutParser

from deck_assembler import DeckAssembler
from parsed_callout import ParsedCallout
from parsed_codeblock import ParsedCodeBlock
from codeblock_parser import CodeblockParser


def main():
    input = Path(".")
    output = Path(".")
    
    assembler = DeckAssembler()
    codeblock_parser = CodeblockParser()
    callout_parser = CalloutParser()
    
    codeblocks: list[ParsedCodeBlock] = []
    callouts: list[ParsedCallout] = []
    
    files = list(input.glob("./**/*.md"))
     
    print(f"Checking {len(files)} files...") 
    
    for file in files:
        with file.open("r") as f:
            
            contents = f.read()
            
            codeblocks.extend(
                codeblock_parser.parse_text(contents, path=file) 
            )
            
            callouts.extend(
                callout_parser.parse_text(contents, path=file) 
            )
            
    print(f"Found 'anki' {len(codeblocks)} codeblocks")

    print(f"Found {len(callouts)} callouts")
   
    decks = {}    
    
    assembler.add_notes_from_codeblocks(codeblocks, decks)
    assembler.add_notes_from_callouts(callouts, decks)
         
    package_name = "deck_package.apkg" 
    
    package_path = output / package_name 
        
    genanki.Package(decks.values()).write_to_file(package_path.absolute())
    
    print(f"Created {package_path.absolute()}")

if __name__=="__main__":
    main()