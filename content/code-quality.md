title: Python Code Quality Setup - Simple and Efficient
date: 2024-10-05
author: Adriana Vasiu
category: development


### Introduction

This is a concise and opinionated post on code quality for python. It covers the following:

- what code quality is 
- tools to use -> [black](https://black.readthedocs.io/en/stable/), [flake8](https://flake8.pycqa.org/en/latest/) and [mypy](https://mypy.readthedocs.io/en/stable/)
- how to integrate those tools in the software development lifecycle

### Code quality? As many opinions as stars in the sky.

The code quality space is one of the most opinionated technical spaces I know. 
Why? Because code quality is to some degree subjective. And it means a lot of things!

In the last few years I joined a lot of projects midway. In more than 50% of the cases, running code quality 
tools was not part of the development lifecycle. Especially in the beginning, the setup for this is cheap.
I didn't understand why code quality checks were not in place. 
But I listened to the teams, and I learnt why. There are a couple of reasons:

- there was no agreement on what code quality actually is -> to avoid disagreement, everyone kind of did what worked for them
- some people thought about code quality as purely stylistic -> this was quickly becoming less of a priority. In the end, this was not affecting production right?

### How do you come up with a simple yet very efficient setup?

When I understood the above, my arguments for introducing code quality tools became convincing and I got agreement on the following.

- At a minimum, code quality means:
    - the code should do what it's supposed to do 
    - the code is easy to read
    - there is no unused code lying around
- We will focus on tools that are concerned with more than style. They will detect unused code, unused imports and verify data type mismatches.
- In terms of style, we will use a tool just so that we don't keep re-formatting each other's changes when we do a PR, because
  each of us have slightly different preference or because our IDE does it for us. One style, no necessary re-formatting.

Once this agreement was in place, it was very easy to choose the tools and settings and integrate them in the development lifecycle.
 
### Tools and Settings

Here is a concise list of tools that I used successfully in practice.

#### Black for formatting

**How to install** 

`poetry add black`

**How to set up**

[Black](https://black.readthedocs.io/en/stable/) has good documentation and can be customised easily with your own settings.
Here are some basic settings for black, that you can add directly in your project's `.toml` file:

```toml
# pyproject.toml

[tool.black]
line-length = 120 # in practice, I find this length working the best. You can work with this in almost any screen size
exclude = ".*(<dir1|dir2>)/.*" # add here auto-generated code and so on, db migrations etc. 
```

**How to run**:

Let's assume you have this code sample:

```python
import time


def func_not_using_time():
    unused_space = "space"    + "more space"
    print('some single quotes space')
```

After you run `poetry run black <source directory>` you will get this:

```python
import time


def func_not_using_time():
    unused_space = "space" + "more space"
    print("some single quotes space")
```

All black did in this instance was to remove some spaces and replace quotes with double quotes. 
It can do much more formatting, depending on the settings and issues encountered. 
The point here is that `black` is concerned with style only. 
It doesn't remove automatically unused imports so there is no risk that it will modify automatically the behaviour of the code.

#### Flake8 for linting

**How to install**

`poetry add flake8`

**How to set up**

In order to make [flake8](https://flake8.pycqa.org/en/latest/) work with your `pyproject.toml` configuration you need to do two steps.

Add the settings into the `pyproject.toml`.

```toml
  # pyproject.toml
  
  [tool.flake8]
  max-line-length = 120
  count = true
  exclude = ".*(<dir1|dir2>)/.*"
  ignore = "W503,E203"
```

Install the [flake8-pyproject](https://pypi.org/project/Flake8-pyproject/) plugin by running `poetry add flake8-pyproject`.
Without this plugin, settings like `max-line-length` will not be respected. 
  
If there are rules that you don't agree with, you can easily add them to the ignore list above.
For example, my preferred setup is to ignore:

- [W503](https://www.flake8rules.com/rules/W503.html) - line break occurred before a binary operator.
- [E203](https://www.flake8rules.com/rules/E203.html) - whitespace before ':' -> this one is a rule that conflicts with the `black` formatter.
  I prefer to let the formatter run and ignore this check for the linter.

For a full list of `flake8` rules have a look [here](https://www.flake8rules.com/).

**How to run**

Let's assume you have the same simple code sample that was formatted with `black`:

```python
import time


def func_not_using_time():
    unused_space = "space" + "more space"
    print("some single quotes space")
```

When you run `poetry run flake8 --show-source --statistics --count <source directory>` you get this result:
```shell
    unused_space = "space" + "more space"
    ^
1     F401 'time' imported but unused
1     F841 local variable 'unused_space' is assigned to but never used
2
```

The linter prompts you that you have unused imports and variables, but it doesn't fix anything for you. 
When you go in and remove the unused code the linter script will just exit with zero. 

#### Mypy for static type checking

**How to install**

`poetry add mypy`

**How to set up**

[Mypy](https://mypy.readthedocs.io/en/stable/) supports `.toml` configuration as well, so you can add your settings 
in `pyproject.toml`.

```toml
# pyproject.toml
[tool.mypy]
exclude = [
    "^one\\.py$",  # TOML's double-quoted strings require escaping backslashes
    'two\.pyi$',  # but TOML's single-quoted strings do not
    '^three\.',
]
```

Have a look [here](https://mypy.readthedocs.io/en/stable/config_file.html) at the list of settings that `mypy` supports.

By default, `mypy` enables a lot of [error codes](https://mypy.readthedocs.io/en/stable/error_code_list.html).
Start from this list and customise any settings if needed. 

**How to run**

If you have no [type hints](https://docs.python.org/3/library/typing.html) for your code, `mypy` won't detect any issues, but 
let's look at a code sample that has some type hints already defined:

```python
import random
from typing import Optional

def return_random_number_in_range(range_threshold: int, max_range: int = 10) -> int:
    """
    The aim of this function is to return a random number in the range (0, range_threshold)
    and not exceed max_range.
    """
    if range_threshold > max_range:
        return None

    return random.randint(0, range_threshold)

return_random_number_in_range(5)
```

When you run `poetry run mypy <source directory>` you will get one error:

`mypy_test.py:11: error: Incompatible return value type (got "None", expected "int")`.

So at this point `mypy` already detected that you are not handling a scenario correctly. 
If a caller of this function adds the result to another `int` let's say, they will immediately fail when the function returns `None`.

If you call the function with the wrong input: `return_random_number_in_range("5")` you get an extra error:
`mypy_test.py:16: error: Argument 1 to "return_random_number_in_range" has incompatible type "str"; expected "int"`.

So `mypy` detects straight away data mismatches, before you even run your code. 

### Development lifecycle

Setting up the tools correctly for your use case is very important, but an equally important aspect is the ease of usage
in your development lifecycle. If you find out about failures too late for example, after your code went through reviews and 
CI tests, it can be frustrating. 

What worked very well for me is:

- having a [pre-commit hook](https://git-scm.com/book/ms/v2/Customizing-Git-Git-Hooks) installed on the local machine
  that runs the `black` formatter and then lints and checks the types. 
- having the same format, lint and type checks run on the CI, before the tests are run. I use `make` tasks
  for all these, and if your CI uses `docker` you can combine `make` and `docker-compose` 
  with the [3 musketeers](https://3musketeers.pages.dev/guide/) approach.

### Summary

- Once you agree with your team on what code quality means, setting up the tools is the easy part.
  Especially if you integrate them in your development lifecycle from the very beginning, they come at a very low cost.
- Code quality tools not only help you prevent bugs, or prompt you on removing unused code,
  but they also help the team avoiding re-formatting each other's code.
- Having code quality checks in place prevents your code for falling into patterns as described in the [broken windows theory](https://en.wikipedia.org/wiki/Broken_windows_theory).



