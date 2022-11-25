from callout_parser import CalloutParser


def test_parsing_of_one_callout():
    parser = CalloutParser()

    content = '''
some irrelevant text
> some irrelevant quote

> [!NOTE] Title attribute1:value1 attribute2:value2 attribute3
> Contents Contents
> Contents2
some irrelevant text
> some irrelevant quote
some irrelevant text
    '''
    
    callouts = parser.parse_text(content, path=None)
    
    assert len(callouts) == 1
    
    callout1 = callouts[0]
   
    assert callout1.type == "NOTE"
     
    callout1_content = callout1.content.splitlines()
    
    assert len(callout1_content) == 2
    
    assert callout1_content[0].strip() == "Contents Contents"
    assert callout1_content[1].strip() == "Contents2"


def test_parsing_of_multiple_callouts():
    parser = CalloutParser()

    content = '''
some irrelevant text
> some irrelevant quote

> [!NOTE] Title attribute1:value1 attribute2:value2 attribute3
> Contents Contents
> Contents
some irrelevant text
> some irrelevant quote
some irrelevant text

> [!WARNING] Title2 attribute1:value1 attribute2:value2 attribute3
> Contents2 Contents2
> Contents2
> Contents2 Contents2 Contents2
    '''
    
    callouts = parser.parse_text(content, path=None)
    
    assert len(callouts) == 2
    
    callout1 = callouts[0]
    callout2 = callouts[1]
    
    assert callout1.type == "NOTE"
    assert callout2.type == "WARNING"
    
    callout1_content = callout1.content.splitlines()
    callout2_content = callout2.content.splitlines()
    
    assert len(callout1_content) == 2
    
    assert callout1_content[0].strip() == "Contents Contents"
    assert callout1_content[1].strip() == "Contents"
    
    assert len(callout2_content) == 3
    
    assert callout2_content[0].strip() == "Contents2 Contents2"
    assert callout2_content[1].strip() == "Contents2"
    assert callout2_content[2].strip() == "Contents2 Contents2 Contents2"