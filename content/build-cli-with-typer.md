title: How to Build a Simple CLI Tool in Python with Typer
date: 2024-11-14
author: Adriana Vasiu
category: development

### Introduction

Over the years, I built CLI tools with [click](https://click.palletsprojects.com/en/stable/), 
[docopt](https://docopt.readthedocs.io/en/latest/) and [argparse](https://docs.python.org/3/library/argparse.html).

I decided to give [typer](https://typer.tiangolo.com/) a go because I saw some of the CLI tools built with it and I liked the output.

### How to install typer

I install everything via [poetry](https://python-poetry.org/) these days, it's my go-to tool for dependencies 
and virtual environments: 

```poetry add typer```

### How to create a simple command

For this blog post I wanted to choose something very simple and something related to a topic that I enjoy. 
So I built this CLI application called `scriptor` that helps me with my writing.

Let's create one command that writes some text into a file, and one that reads the file.

```python
import typer

app = typer.Typer()

@app.command()
def write(text: str):
    with open("book.txt", "a") as f:
        f.write(text + "\n")


@app.command()
def read():
    with open("book.txt", "r") as f:
        print(f.read())

if __name__ == "__main__":
    app()
```
^^ `scriptor.py`

Let's run `scriptor` with the `--help` option:

```shell
➜ poetry run python scriptor.py --help

 Usage: scriptor.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                                                  │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                                           │
│ --help                        Show this message and exit.                                                                                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ read                                                                                                                                                                                                     │
│ write                                                                                                                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

And if we zoom in on one command:

```shell
➜ poetry run python scriptor.py write --help

 Usage: scriptor.py write [OPTIONS] TEXT

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    text      TEXT  [default: None] [required]                                                                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

Let's write something and then read it back:

```shell
➜  poetry run python scriptor.py write "I am writing in my book."
➜  poetry run python scriptor.py write "Chapter 1. The Beginning."
➜
➜  poetry run python scriptor.py read
I am writing in my book.
Chapter 1. The Beginning.
```

### How to create a simple command with options

Let's say that we want to add a command that:

- by default counts the number of words we just wrote
- it accepts one or multiple words and outputs their frequency - this is optional

When you first look at typer, the only thing you need to get used to is how you can define your input for the commands.
The implementation of the command is nothing more than adding your custom logic.
Let's work on the requirement above and create a command called `count` and work on the parameters step by step:

Step 1. Decide what the input looks like in typer

By default, a CLI option in typer is optional, as opposed to a CLI argument. So we can use the `typer.Option` to 
pass in data to the command line. The option will look like this: `--word <my-word>`.
In typer, you can pass an option multiple times `--word <word-1> --word <word-2>` so this is suited for our requirement 
to accept more than one word. 

Based on this, our parameter for the command will look like this:
```python
word: Annotated[<some-type-to-define>], typer.Option()] = None
```

Please note that typer recommends to use [Annotated](https://docs.python.org/3/library/typing.html#typing.Annotated)
for adding content-specific metadata to an annotation, but if you prefer, you can type your arguments without it. 

Step 2. Define the type for the `word` parameter

The value that comes back from the option will be a list of strings, which is also optional so our type will be:
`Optional[list[str]] `.

Putting everything together results in the following definition for the command:

```python
@app.command()
def count(word: Annotated[Optional[List[str]], typer.Option()] = None):
    ...
```

Now let's add some basic implementation for the count and try it out:

```python
@app.command()
def count(word: Annotated[Optional[List[str]], typer.Option()] = None):
    with open("book.txt", 'r') as f:
        count_items = collections.Counter(f.read().split())
        if not word:
            print(sum(count_items.values()))
        else:
            for w in word:
                print(f"The word \"{w}\" appears {count_items.get(w, 0)} times")
```

The command output will look like this:

```shell
➜  poetry run python scriptor.py count
10
➜ poetry run python scriptor.py count --word I --word write
The word "I" appears 1 times
The word "write" appears 0 times
```

At the minimum, this is all you need to do to create a command with options. 

### How to create subcommands

Let's assume that we come back to our requirements for the `count` command and want to also count lines, not just words. 
This is a good candidate for adding two subcommands:

- one that counts words: `poetry run python scriptor.py count words`
- one that counts lines: `poetry run python scriptor.py count lines`

The key here is to make the `count` command be a typer app, so that we can append commands to it:

```python
count_app = typer.Typer()
app.add_typer(count_app, name="count")
```

Then we can create the two subcommands like this:

```python
@app.command()
def count():
    ...


@count_app.command("words")
def count_words(word: Annotated[Optional[List[str]], typer.Option()] = None):
    with open("book.txt", 'r') as f:
        count_items = collections.Counter(f.read().split())
        if not word:
            print(sum(count_items.values()))
        else:
            for w in word:
                print(f"The word \"{w}\" appears {count_items.get(w, 0)} times")


@count_app.command("lines")
def count_lines():
    with open("book.txt", 'r') as f:
        count_items = collections.Counter(f.read().split("\n"))
        print(f"The number of lines in the book is: {sum(count_items.values())}")
```

The most important thing that changes here is that `count_words` and `count_lines` functions are now annotated
with `@count_app.command("words")` instead of `@app.command("words")`. 
And that's it, you now have two subcommands on your `count` command. 

Let's run one of them and check the output:

```shell
➜  poetry run python scriptor.py count lines
The number of lines in the book is: 3
```

If we run the `--help` option on `count` we get:

```shell
➜  poetry run python scriptor.py count --help

 Usage: scriptor_v2.py count [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ lines                                                                                                                                                                                                    │
│ words                                                                                                                                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

We can then zoom in into one subcommand with the `--help` option:

```shell
➜  poetry run python scriptor.py count words --help

 Usage: scriptor_v2.py count words [OPTIONS]

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --word        TEXT  [default: None]                                                                                                                                                                      │
│ --help              Show this message and exit.                                                                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Summary

- typer is simple and intuitive to write once you understand how it's using the type annotations.
- it's very easy to setup for simple commands.
- it's very concise.
- the output is nicely formatted.
- has clear documentation.
- follows some of the design principles from [fastAPI](https://fastapi.tiangolo.com/) so if you are familiar with fastAPI you will
  like it instantly.











