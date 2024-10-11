title: Python Essentials - REPL
date: 2024-10-11
author: Adriana Vasiu
category: development

### Introduction

This is the first blog post from a series I am calling "Python Essentials". Every time I am working on python projects
I have a list of very simple tools and techniques that I always go to. 
Why? Because they are powerful through their simplicity. 

And this week's "Python Essential" is the [REPL](https://docs.python.org/3/tutorial/interpreter.html) because I was 
inspired by the python `3.13.0` release and the fact that it brought a lot of improvements to it. 

REPL, an acronym for "read–eval–print loop" is nothing other than an interactive interpreter shell.

Weather you are taking a new python feature for a test drive, or you can't quite remember how something works, 
REPL is your most straight forward tool at hand.
Want to work offline for a while or skip opening the python docs all the time? REPL is there for the take.

### How do you open an interactive shell?

In your terminal, run `python`. Depending on the default version of python you have set in your system, the 
interactive shell will look something like this:
```shell
➜  ~ python
Python 3.13.0rc3 (main, Oct 10 2024, 19:01:15) [Clang 15.0.0 (clang-1500.1.0.2.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

I am using `pyenv` for installing new versions of python and `python3.13` is not available just yet in `pyenv` releases.
The python version I have just installed and set as my global python version is `python3.13.0rc3` so that is what you are seeing
in the interactive prompt. 

So let's start interacting with it!

### How to try things out quickly

You can use the REPL to try things out, without the need to set up an IDE or to even create a python file.

Let's say that you don't remember exactly how string slicing works with a stride/step, and you want to test it out:

```shell
>>>
>>> s = "moose"
>>> s[1::2]
'os'
>>>
```

You don't even need to print anything if you are just testing a statement, the result of it is printed in the terminal.

You can try out entire functions or classes. Let's say that you want to remember how to create a simple timer decorator with
`functools`:

```shell
>>>
>>> import functools
>>> import time
>>> def timer(func):
...     @functools.wraps(func)
...     def wraps_timer(*args, **kwargs):
...         start_time = time.perf_counter()
...         result = func(*args, **kwargs)
...         end_time = time.perf_counter()
...         run_time = end_time - start_time
...         print(f"{func.__name__} run in {run_time:.4f} secs")
...         return result
...
...     return wraps_timer
>>>
>>> @timer
>>> def my_func():
...     return sum([x for x in range(10_000)])
>>>
>>> my_func()
my_func run in 0.0031 secs
49995000
>>>
```

When you type in a function, the interpreter will automatically add tabs for you and you can see you are in the context of
that function because the prompt is changing to `...`. 

The interpreter is actually so useful that when you do a typo, it nudges you in the right direction:

```shell
>>>
>>> prant("moose love forest")
Traceback (most recent call last):
  File "<python-input-22>", line 1, in <module>
    prant("moose love forest")
    ^^^^^
NameError: name 'prant' is not defined. Did you mean: 'print'?
>>>
```

### How to do introspection

Another very useful feature of the REPL is to be able to see what a standard python module offers. 
Or how you can use some of the core functionality.

Let's assume you want to see what is in the `collections` module. 
You can import it in the interactive interpreter and use `dir` to explain it.

```shell
>>>
>>> import collections
>>> dir(collections)
['ChainMap', 'Counter', 'OrderedDict', 'UserDict', 'UserList', 'UserString', '_Link', '_OrderedDictItemsView', '_OrderedDictKeysView', '_OrderedDictValuesView', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', '_chain', '_collections_abc', '_count_elements', '_deque_iterator', '_eq', '_iskeyword', '_itemgetter', '_proxy', '_recursive_repr', '_repeat', '_starmap', '_sys', '_tuplegetter', 'abc', 'defaultdict', 'deque', 'namedtuple']
>>>
```

Now you can see everything that the `collections` module contains.
And you can go deeper and print the docs of the module for example:

```shell
>>>
>>> collections.__doc__
""This module implements specialized container datatypes providing\nalternatives to Python's general purpose built-in containers ..."
>>>
 .... 
```

You can even invoke `help` to find out more about a specific module, class, function etc.

The help command will produce an output that starts like this:

```shell
>>> help(collections.ChainMap)
```

```shell
Help on class ChainMap in module collections:

class ChainMap(collections.abc.MutableMapping)
 |  ChainMap(*maps)
 |
 |  A ChainMap groups multiple dicts (or other mappings) together
 |  to create a single, updateable view.
...
```

You can go even further and use the `help` utility itself:

```shell
>>> help
>>> Welcome to Python 3.13's help utility!
...
help>
```

As you can see above, after typing `help` in the interactive shell, the prompt is changing to `help>`. 

Typing `topics` from the `help>` prompt will give you a list of all the topics you can explore. 

This is a very powerful tool to discover the core python capabilities in a very concise view!


```shell
help> topics
Here is a list of available topics.  Enter any topic name to get more help.

ASSERTION           DEBUGGING           LITERALS            SEQUENCES
ASSIGNMENT          DELETION            LOOPING             SHIFTING
ASSIGNMENTEXPRESSIONS DICTIONARIES        MAPPINGMETHODS      SLICINGS

<A lot more topics here...>

```

```shell
help> ASSERTION
The "assert" statement
**********************

Assert statements are a convenient way to insert debugging assertions
into a program:

   assert_stmt ::= "assert" expression ["," expression]
...   
```

### Other useful commands for the REPL

Besides trying things out quickly and doing introspection, you can use it as a calculator:

```shell
>>>
>>> (123-34)*3**2
801
>>>
```

And especially when you set up a new project, checking things like the `PYTHONPATH` is straightforward:

```shell
>>> import sys
>>> sys.path
['<a list of paths here>']
>>>
```

The `sys` module has a lot more functionality in it, so if your curious about your python installation you can use `dir(sys)` to explore it.

And if you want to remind yourself why you love `python` so much, you can always look at the Python Zen:

```shell
>>>
>>> import this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
>>>
```

### Summary

- REPL is the fastest way to get familiar with the capabilities of the language, try things out and learn something new.
- Is a tool built with simplicity in mind and is constantly improving. 
- Is the first tool I recommend to anyone starting out their journey in learning `python`.

 








