# markdown-to-anki
Parses markdown elements into cloze anki notes and assembles them into an anki package using [genanki](https://github.com/kerrickstaley/genanki).

## Usage
This script can handle codeblocks or [obsidian callouts](https://help.obsidian.md/How+to/Use+callouts).

Create some anki code blocks or callouts in your markdown files with unique `name` and `deck` (note the `anki` attribute in codeblock):

~~~markdown
```anki name:strings deck:programming_fundamentals
	{{c1::Strings}} are sequences of {{c2::characters}}.
```

or using markdown codeblock:

```markdown anki name:strings deck:programming_fundamentals
	{{c1::Strings}} are sequences of {{c2::characters}}.
```

Note the `anki` attribute in the header of the codeblock. It is required.

Some text..

> [!summary]+ name:obsidian deck:general
> Use {{c1:obsidian}} to record notes
>
> Because its convenient.
~~~

Run `python markdown_to_anki.py --help` to see usage instructions and defaults. Specify input and output dirs as follows: `python markdown_to_anki.py --input_dir /path/to/input --output_dir /path/to/output`.

Then import the package into anki.

If you want other markdown elements to be handled, feel free to submit an issue or open a discussion.
