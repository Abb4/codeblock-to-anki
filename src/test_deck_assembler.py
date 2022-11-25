from pathlib import Path
import genanki
from callout_parser import CalloutParser
from deck_assembler import DeckAssembler, quick_hash
from codeblock_parser import CodeblockParser

# FIXME currently assemble_deck_from_codeblocks writes to disk which is bad for testing, split the method and rewrite the test
def skipped_test_deck_creation():
    assembler = DeckAssembler()
    
    parser = CodeblockParser()
   
    content = '''
    ```anki name:test_note deck:test_deck
        {{c1::Cloze1}} before {{c2::cloze2}}.
        some more code
    ```
    
    ```anki name:test_note deck:test_deck2
        {{c1::Cloze1}} before {{c2::cloze2}}.
        some more code
    ```
    
    ```anki name:test_note2 deck:test_deck
        {{c1::Cloze1}} before {{c2::cloze2}}.
        some more code
    ```

    '''
    
    codeblocks = parser.parse_text(content, None)
    
    assembler.assemble_deck_from_codeblocks(codeblocks, None)


# FIXME currently assemble_deck_from_codeblocks writes to disk which is bad for testing, split the method and rewrite the test
def skipped_test_deck_creation_from_callouts():
    assembler = DeckAssembler()
    
    parser = CalloutParser()
   
    content = '''
> [!summary]+ name:strings2 deck:programming_fundamentals2
> {{c1::Strings}} are {{c2::Nice}}
'''
    
    callouts = parser.parse_text(content, None)

    decks = {}    
    
    assembler.add_notes_from_callouts(callouts, decks)
    
    package_name = "deck_package2.apkg" 
    
    output = Path(".")
     
    package_path = output / package_name 
        
    genanki.Package(decks.values()).write_to_file(package_path.absolute())
    
    print(f"Created {package_path.absolute()}")
    
    assert False

def test_quick_hash():
    note1_name = "My Note"
    note2_name = "My Note" # test that hashes correctly use values for equality
    note3_name = "My other Note"
    
    assert quick_hash(note1_name) == quick_hash(note2_name)
    assert quick_hash(note1_name) != quick_hash(note3_name)
    
def test_getting_attributes_from_headers():
    assembler = DeckAssembler()
    
    attributes = ["attribute1:value1", "attribute2:value2", "attribute3"]
    
    assert assembler.get_attribute_from_codeblock_headers(attributes, "attribute1") == "value1"
    assert assembler.get_attribute_from_codeblock_headers(attributes, "attribute2") == "value2"
    assert assembler.get_attribute_from_codeblock_headers(attributes, "attribute3") == None
    assert assembler.get_attribute_from_codeblock_headers(attributes, "unknown") == None

def test_getting_attribute_values():
    assembler = DeckAssembler()
    
    attributes = ["attribute1:value1", "attribute2:value2", "attribute3"]
    
    assert assembler.get_attribute_value_by_name(attributes, "attribute1") == "value1"
    assert assembler.get_attribute_value_by_name(attributes, "attribute2") == "value2"
    assert assembler.get_attribute_value_by_name(attributes, "attribute3") == None
    assert assembler.get_attribute_value_by_name(attributes, "unknown") == None
    