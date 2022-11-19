# codeblock-to-anki
Parses markdown code blocks and assembles them into an anki package using [genanki](https://github.com/kerrickstaley/genanki).

## Usage
Create some anki code blocks in your markdown files with unique `name` and `deck` (note the `anki` attribute):

~~~
```anki name:strings deck:programming_fundamentals
	{{c1::Strings}} are sequences of {{c2::characters}}.
```
~~~

Run `python path/to/src/codeblock_to_anki.py` in the directory where you notes lie. All notes in the directory and child directories will be assembled into anki cloze notes and written into a package.

Import the package into anki.

Contributions are very welcome.