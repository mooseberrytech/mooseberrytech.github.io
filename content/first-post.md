title: Why pytest-bdd?
date: 2024-09-12
author: Adriana

### Introduction
This blog posts doesn't advocate for BDD testing. If you are already convinced that you need some BDD tests as part of your software development lifecycle and you have been looking around for what frameworks to choose, than this post might be useful for you.

### Why use pytest-bdd?
I have used a lot of BDD frameworks in the past. The ones that I remember are Lettuce, Freshen and Behave. All of them worked ok. They did the job. 
Behave for example, is very feature reach, it offers features like data tables which is particularly useful for building data driven tests. All that worked well.

But each of those frameworks came in short in some aspects. I am not going to focus on a feature by feature comparison on all these frameworks. 
Instead, I am going to share what I would like to see in a testing framework and how [pytest-bdd](https://pytest-bdd.readthedocs.io/en/stable/) measures against that. 

Here are the main aspects that are important to me:
- it is simple
- it is easy to run
- encourages explicit behaviour rather than implicit
- has an active support community
- comes with good documentation
- supports running scenarios in parallel

Let's address each of the points above and see why pytest-bdd measures against them.

#### Simple

What does it take to set up the framework?
Step 1. Install the package. (Let's assume you are using poetry.)
```commandline
poetry add pytest-bdd
```
Step 2. Create your test structure.

```commandline
tests
   features
      demo.feature
   __init__.py
   test_demo.py
```
Step 3. Create a test feature with one scenario.

```
Feature:
  Scenario: Run a demo for the blog
    Given I have a blog with 2 posts
    When I publish a new post
    Then my blog will contain 3 posts
```
^^ `demo.feature`
Step 4. Create the test that runs the feature and implement the scenario steps.
```python

from pytest_bdd import scenarios, given, when, then, parsers

scenarios("features/demo.feature")


@given(parsers.parse("I have a blog with {number_of_posts} posts"))
def given_blog(number_of_posts):
    ...


@when("I publish a new post")
def when_publish():
    ...


@then(parsers.parse("my blog will contain {number_of_posts} posts"))
@then(parsers.parse("my blog will contain {number_of_posts} post"))
def check_blog_posts(number_of_posts):
    ...

```
^^ `test_demo.py`

This is it! You have everything you need to start implementing your first test.

#### Easy to run

Tests written with `pytest-bdd` take advantage of the `pytest` runner, and the autodiscovery of tests that it provides.
Run your test with `pytest` (This assumes `pytest-bdd` was installed with poetry.):
`poetry run pytest`
This will automatically find all files named with the prefix `test_` in the `tests` directory.

#### Explicit behaviour rather than explicit

I like that pytest makes the state management of your steps obvious and explicit.
There is no context object that is passed implicitly in every step, `pytest-bdd` makes use of [fixtures](https://docs.pytest.org/en/6.2.x/fixture.html)
to manage state and fixtures are explicit, modular and scalable.
Here is an example of a fixture passed from one step into the next.

```python

@dataclasses.dataclass
class Blog:
    posts: int = 0


@pytest.fixture
def blog():
    ...


@given(parsers.parse("I have a blog with {number_of_posts} posts"), target_fixture="blog")
def given_blog(number_of_posts):
    return Blog(posts=int(number_of_posts))


@when("I publish a new post")
def when_publish(blog):
    blog.posts += 1


@then(parsers.parse("my blog will contain {number_of_posts} posts"))
@then(parsers.parse("my blog will contain {number_of_posts} post"))
def check_blog_posts(number_of_posts, blog):
    assert blog.posts == int(number_of_posts)
```
^^ `test_demo.py`
The fixture `blog` is overriden in the `given_blog` step, then passed into the next `when_publish` step and re-used 
in the `check_blog_posts` step for verification.
The state is defined explicitly, you know which fixture you are targeting or modifying.

#### Community and Documentation
The [pytest-bdd](https://github.com/pytest-dev/pytest-bdd) codebase and documentation are frequently updated. 
There are quite a few issues logged and discussed, and sometimes workarounds are proposed. 
There are also a lot of video and written tutorials published online or how to use the framework.

#### Supports Running Scenarios in parallel

`pytest-bdd` integrates with [pytest-xdist](https://pytest-xdist.readthedocs.io/en/stable/).
Install `pytest-dist` (Let's assume you are using poetry.):
```commandline 
poetry add pytest-xdist
```
If you want to distribute tests across multiple CPUs in order to optimise test execution, run multiple worker processes:
```commandline
poetry run pytest -n auto
```

#### Summary
If you are looking for a BDD framework that you want to start using in minutes and especially if you are 
already using the feature rich `pytest` framework, give `pytest-bdd` a try. 
It's the framework that will allow you to write steps in the most python way and allows you to run all your tests with one command.




