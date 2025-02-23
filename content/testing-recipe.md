title: Writing Good Tests is not an Easy Task
date: 2025-02-23
author: Adriana Vasiu
category: testing

Being a consultant means I do see a lot of projects with various levels of code quality and testing.
There is a lot to say about how to measure the quality of a software project, that in itself is worth a separate blog post,
but in essence, quality is about how well a project serves its purpose for the business. 

The best projects I have seen in that respect are projects that have excellent tests. 
If you know what you are testing, you know what you are delivering and why. 

The following test characteristics are key to good testing. 

### Simple and Obvious

Writing tests is actually a different paradigm from writing code for production.

When I design code I think about how to avoid repeatability and how to build for extensibility. 
With tests, I avoid any logic that might cause me introducing bugs in the tests themselves. There are techniques that can be used 
to avoid some of the repeatability, like parametrizing tests with different data sets. But beyond that, I don't 
introduce any logic that takes away from the simplicity of the tests. 

My tests focus always on the code itself, how to test every scenario, their aim is just that. 
They are so simple that anyone that reads them can figure out exactly what they are doing and how. 
There is nothing smart or sophisticated about my tests.
Any test utilities that I build, for example mocks, are doing very little. Just enough to emulate what I want to assert.

When I say that tests should be obvious, I mean it. Make them as explicit as you possibly can. 
So obvious that they should be easy to understand even when you are exhausted or distracted. 

### Living documentation

The first thing I look at when I open a new codebase are the tests. If I can read them and understand what they are testing, 
this reduces my cognitive load on understanding the project. 
Is true that you can not know everything about a project just from tests, you will still need to understand architecture 
or how the software is delivered into production, but the tests tells a compelling story about the code. 

If tests are small, with descriptive names, you know that the developers have focused on the details of their code, and they truly understand
how the code evolves. You can read what the code is supposed to do in certain situations, you can get an idea about what data 
your code is handling. 

Tests are the best documentation you can produce while evolving your code. If you have functional tests in BDD style as well, then the living documentation
is very much improved and can be read by anyone in the business, with or without coding experience.

### Independent and Isolated

Whenever I write one test, I write it in complete isolation. My test should be able to run by itself and with other tests. 
There is no order in which my tests should be run. The same setup should work for one or one hundred tests. 

When you encounter tests that affect other tests, by modifying some setup, or creating some state, the confidence in what the test
is verifying is greatly reduced. You cannot predict any side effects, so you should avoid them at all costs. 
Avoid this, and you will avoid intermittent test failures and test debugging nightmares.

If your tests depend on state - e.g. you are testing with an in memory database which needs to be migrated first, then make that setup external 
to the test itself. The setup should be part of your test framework. The test itself should have no control on any shared state.

### Focused

I write my tests as focused as possible because when I refactor code and I accidentally break something, I want to see
exactly what the impact is. If I have to debug through the test itself to find out what I actually broke than that is a big sign
that my test is way too complicated and is not focused on a specific scenario.

Especially unit tests, they should be small, focused and assert one specific thing. This is not about having one assert statement, you might
have more than one, because you are verifying some more complex output data for example, but the test should zoom in on one concern. 

Let's take a method that does two things (arguably it does too much) - updates two different data models at once. 
Your should have one test for each model update. If you do a refactoring and introduce a bug related to just one model, only the test that looks at updating that model
should fail, you shouldn't need to look at anything else.

Test one thing, test it well, do not look back. 

### Portable

I consider portability to be a very important aspect of good tests. In practice, this is often overlooked.

When functional tests are run in a repeatable and portable way, in all environments - local, ci, deployed environment - you have a reliable way
to assert your assumptions. 
I specifically mention functional here, because non-functional tests, of course, depend on the specification of their target environment.

If you are aiming to run your tests for example in docker, deployed as a kubernetes job, targeting a system run in kubernetes,
than package and run your tests locally in docker. Setup the whole stack you are testing against, with mock dependencies, in docker-compose
and run the tests in docker. 
Your CI should do that even before your code reaches the cluster.

### Non-Brittle 

Test brittleness is a tricky subject because is not always an indicator that your tests are wrongly designed, most of the time 
is an indicator that your code is coupled and cannot be tested in small units. 

Either way, if you modify one line of code, and you break a lot of tests, you have a problem.
This is when you can use the tests to actually drive better design for your code, decouple it, make it easily testable. 

Another cause for test brittleness is when tests are forced to make use of a lot of patching. Imagine that you change the name of 
one method, and you break not only the tests for that method but a lot more. That means that you should make use of dependency injection in your code.

The main thing about brittleness of the tests is the fact that it drives code improvements when tackled correctly. 

Another thing to note here is that you wouldn't need to deal with brittleness if you started with the tests.
So consider Test Driven Development if you want to develop code that is easily testable. 

## Summary
 
I find that writing good tests can be more challenging that writing good code sometimes.

There are good examples, tutorials and a lot of libraries that can help you design your tests better, but you need to think of them 
as a great asset when you develop, not an afterthought. 
The more you refine your testing strategy the more thought you put in what your code actually does and how it's serving its purpose.

A strong test coverage is the foundation of your code's sustainability through continuous refactoring and simplification. 
















