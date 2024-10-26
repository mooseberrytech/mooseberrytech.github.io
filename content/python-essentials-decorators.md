title: Python Essentials - Decorators
date: 2024-10-26
author: Adriana Vasiu
category: development

### Introduction

Decorators are a tool for making your python code more readable, and it also helps you to stick to the DRY principle. 
Whether you add your own, or you are using a decorator provided by a library or framework, understanding how decorating works in python 
is an essential tool in your toolbox. 

### What are decorators?

The simplest definition I could find is when we look at the decorators applied to functions:

*A decorator is a function that wraps another function, and it modifies its behaviour.*

Here is a very simple example:

```python
def my_decorator(func):
    def wrapper():
        print("Something important is about to happen")
        func()
    return wrapper

def my_example_function():
    print("I am doing something important")

```

In the example above you have:

- a function that does something
- another function that uses the `my_example_function` as an argument, and does something to it. In this case, it prints 
  something before calling the function. This is the decorator. 

When you examine the results in REPL, this is what you get:

```shell
>>>
>>> decorated_function = my_decorator(my_example_function)
>>> 
>>> decorated_function()
Something important is about to happen
I am doing something important
>>> 
```

There is one thing to notice here, the decorator itself returns a function, so you do need to call it to get the result. 
If you look at the actual `decorated_function` object, you can see that is a function:

```shell
>>> 
>>> decorated_function
<function my_decorator.<locals>.wrapper at 0x102abb560>
>>> 
```

A function can be used as an argument to another function because according to the [python data model](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types)
any data in a python program is an object, including the function itself. 

Modifying a function before it's even invoked is great, but it would be even better if you were able to invoke it directly, and have another way to "decorate" it. 
Imagine you have a function that is called a lot in your codebase, and you want to add some extra logging before it's called, 
without changing the calling code.

This is where the following syntactic sugar comes into play: 

```python
@my_decorator
def my_example_function():
    print("I am doing something important")
```

Then you can invoke the function directly and get the same result:

```shell
>>> 
>>> my_example_function()
Something important is about to happen
I am doing something important
>>> 

```

You would have seen the syntax above in a lot of the frameworks and libraries you are using. It's a heavily used 
feature in the python ecosystem.

### How to write your own decorators

#### Simple decorators

I included this decorator example in [one of my previous posts on REPL](https://mooseberrytech.co.uk/2024/10/python-essentials-repl.html)
because it's so simple to implement and very useful when you want to measure the time spent on an activity that you don't have granular metrics for.
Or you might want to time a test, or debug the time it takes to make an external call because your client library
doesn't support that already.

```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"{func.__name__} runs in {run_time:.4f} secs")
        return result
    return wrapper_timer

@timer
def my_time_consuming_func(max_range):
    return sum([x for x in range(max_range)])
```

This is the output of the function:

```shell
>>> 
>>> my_time_consuming_func(100_000)
my_time_consuming_func run in 0.0071 secs
4999950000
>>> 
```

One thing to notice in this decorator is that I am using `@functools.wraps(func)` to decorate the `wrapper_timer`.
This is a decorator factory from the [functools](https://docs.python.org/3/library/functools.html#) module that at a minimum,
helps you preserve the function name. 

```shell
>>> 
>>> # with @functools.wraps(func)
>>> my_time_consuming_func.__name__
'my_time_consuming_func'
>>> 
>>> 
>>> # without @functools.wraps(func)
>>> my_time_consuming_func.__name__
'wrapper_timer'
>>> 
```

#### Stacked decorators

Let's assume that our time-consuming function above does a bit more. It throws a `ValueError` for some of the input:

```python
@timer
def my_time_consuming_func(max_range):
    if max_range > 100_000:
        raise ValueError()
    return sum([x for x in range(max_range)])
```

It would be useful to have a decorator that does something when a `ValueError` occurs. For the purpose of illustration,
to keep it simple, the error handler just catches the error and prints something.
So let's define another decorator that does that: 

```python
def error_handler(func):
    @functools.wraps(func)
    def wrapper_error_handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print("An error occurred")
    return wrapper_error_handler
```

What happens if you "stack" the decorators? Let's add the `@error_handler` to the function:

```python
@error_handler
@timer
def my_time_consuming_func(max_range):
    if max_range > 100_000:
        raise ValueError()
    return sum([x for x in range(max_range)])
```

```shell
>>> 
>>> my_time_consuming_func(100_001)
An error occurred
>>> 
```

Ok, so the `error_handler` is applied, but the timer doesn't work. What happened there? 
The order of decorators is important. Python will execute the closest decorator to the function first, in this case `timer`. 
That means that when the `ValueError` occurs, the execution is interrupted and the time will not be printed.
Then the `error_handler` is run and prints that an error occurred.

Let's change the order of the decorators:

```python
@timer
@error_handler
def my_time_consuming_func(max_range):
    if max_range > 100_000:
        raise ValueError()
    return sum([x for x in range(max_range)])
```

```shell
>>> 
>>> my_time_consuming_func(100_001)
An error occurred
my_time_consuming_func runs in 0.0002 secs
>>> 
```

Because we handled the error first, the timer works for the `ValueError` scenario as well. This is very powerful in practice.
You can follow the single responsibility principle for your code by separating different concerns in different decorators, 
tested independently. Then all you need to do is "stack" them.

#### Decorators with arguments

Sometimes you will encounter the situation when you need to pass an argument to the decorator itself, to make it more flexible.
Let's take for example the `timer` decorator above and invent the requirement that sometimes you need to time the function in milliseconds
rather than seconds. Something like this:

```python
@flexible_timer(milliseconds=True)
def my_time_consuming_func(max_range):
    if max_range > 100_000:
        raise ValueError()
    return sum([x for x in range(max_range)])
```

You know from what you have seen so far, that a decorator accepts a function and returns a function, so how does the argument
now come into play?
You need to define a new function that accepts the `milliseconds` argument and returns a decorator right? 
Another level of nesting. Something like this:

```python
def flexible_timer(milliseconds):
    def my_decorator(func):
        ...
    return my_decorator
```

Now you update the code above and replace `my_decorator`, with the `timer` decorator that also accounts for `milliseconds`:

```python

def flexible_timer(milliseconds):
    def timer(func):
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            run_time = end_time - start_time
            # This is the new logic that accounts for the milliseconds parameter
            if milliseconds:
                print(f"{func.__name__} runs in {run_time * 1000:.4f} milliseconds")
            else:
                print(f"{func.__name__} runs in {run_time:.4f} secs")
            return result
        return wrapper_timer
    return timer
```

Let's look at the result when the `flexible_timer` is applied with argument `milliseconds=True` as illustrated above:

```shell
>>> 
>>> my_time_consuming_func(10_000)
my_time_consuming_func runs in 1.4984 milliseconds
49995000
>>> 
```

There are a few things happening here: 

- at the first glance, it seems like the `milliseconds` is not used in the `flexible_timer` function itself. 
  Under the hood, python is using [closures](https://en.wikipedia.org/wiki/Closure_(computer_programming)) to store its value
  so that the inner wrapper can use it.
- since the `timer` decorator is an inner function, you won't be able to use it directly anymore
- the same technique of defining an inner function that returns a function is used here as well, the only difference
  is that the `timer` function is a decorator itself. 

 
#### Class decorators

Yes, you can apply decorators to a whole class. Your intuition would probably tell you that decorating a whole class
will decorate every method in that class, but that's not the case. 
The decorator applies to the instantiation process only. Let's apply the `timer` to the following simplistic class:

```python
@timer
class MyTimeConsumingClass:
    def __init__(self, max_range):
        print('I am creating an instance here')
        self.max_range = max_range

    def my_time_consuming_func(self):
        return sum([x for x in range(self.max_range)])
```

And let's assess the decorated result:

```shell
>>> 
>>> decorated_result = MyTimeConsumingClass(10_000)
I am creating an instance here
MyTimeConsumingClass runs in 0.0001 secs
>>> 
```

A good example of a class decorator that is used often in practice is the `@dataclass` decorator that at a minimum, 
generates an `__init__` method using type annotations:

```shell
>>> 
>>> from dataclasses import dataclass
>>>
>>> @dataclass
... class PersonalDetails:
...     name: str
...     age: int
... 
>>> PersonalDetails(name="Moose", age=5)
PersonalDetails(name='Moose', age=5)
>>>
```

Another popular example on when a class decorator would be useful is when you want to create a singleton.

### Summary

- Decorators help with the DRY and Single Responsibility Principle -> they make your code more readable, less repeatable, easier to test.
- Understanding how decorators work and their order of execution is important to be able to debug and understand code in libraries and frameworks 
  that you are using. Decorators are heavily used in the python ecosystem.
- Decorators can be really powerful, especially when you "stack" them .
- The `functools` module is great to help you build your own decorators.
- Function decorators are the most popular but class decorators can prove very useful as well -> dataclasses and singletons are popular examples.








