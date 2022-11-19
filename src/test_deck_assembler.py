from deck_assembler import DeckAssembler, quick_hash
from parser import CodeblockParser

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
    