title: Having fun debugging bash scripts that exit with 141
date: 2024-11-26
author: Adriana Vasiu
category: automation

# Introduction

This is a very short post on how important it is to be methodical when you debug. 

Recently I had a very short but interesting bash script debugging exercise which reminded me of two important things:

- every output you get as part of the debugging process is important, so you need to pay attention to it
- every step that you take needs to be thought through, don't let appearances full you

# My debugging exercise

A while back I developed a script to run some process in the cluster and just the other day it started failing in our CI 
with `141`even if apparently nothing in that script itself changed. 

Instead of looking directly at the output of the script and taking it from there, I first suspected that something changed 
in the image run on the CI and I went to check that. It turns out that the image was actually updated, but my error had nothing to do with that. 
In hindsight, all I needed to do was to read the exit code. 

So how did I go about debugging this? 

**Step 1.** I looked up what `141` exit code means 

When a script exits with `141`, this means that a `SIGPIPE` signal was sent back to the process that runs the script.

An easy way to test this (this assumes you are on a Unix like system):

- run `sleep 1000` in one of your bash terminals
- get the pid from another terminal using `ps -a` -> let's say your process has pid `<x-pid>` 
- run `kill -SIGPIPE <x-pid>`
- in the terminal you run the `sleep` command, get the last exit code by running `echo $?` -> this will output `141`

**Step 2.** I reminded myself when a `SIGPIPE` is triggered

The `SIGPIPE` signal is sent to a process when it attempts to write to a pipe without a process connected to the other end.

So that means that in my script something has changed in one of the pipes. That most likely means that writing to a pipe
takes too long. 

Debugging the script step by step I narrowed down the issue to a pipe that was doing something like this:
`git tag  --sort=-v:refname | head -n 1`. 

So if the first command takes longer because the fetching of the tags is slow or number of tags has increased, this can 
cause a broken pipe. 

**Step 3.** I looked at the script settings 

In order to reproduce this in the terminal I looked at the settings of my script, and all I needed to do was to set the `pipefail`
option in my terminal: `set -o pipefail`.

**Step 4.** I debugged the pipeline

Is simple to debug a pipeline so for the purpose of this post let's look at this pipeline example:

```shell
➜  ~ (seq 9000; sleep 0.1; seq 9000) | cat | head -c 5
```

In order to see all the outputs you can run this:

```shell
➜  ~ (seq 9000; sleep 0.1; seq 9000) | cat | head -c 5 & echo "${PIPESTATUS[@]}"
```

And you will get an output like this:

```shell
[1] 37362 37363 37365
1
2
3[1]  + 37362 broken pipe  ( seq 9000; sleep 0.1; seq 9000; ) |
       37363 broken pipe  cat |
       37365 done         head -c 5
```

**Step 5.** One possible solution - collect the output of the first command

I am sure there are more solutions to this but the first that came to mind was to collect the output and then process it:

```shell
➜  ~ OUTPUT=$(seq 9000; sleep 0.1; seq 9000)
➜  ~ echo "$OUTPUT" | head -c 5  & echo "${PIPESTATUS[@]}"
[1] 38319 38320
1
2
3[1]  + 38319 done       echo "$OUTPUT" |
       38320 done       head -c 5
```

And that's it, the output is now processed successfully.

# Summary

Even if you have been debugging issues for years, when it's something that you don't debug every day, you tend to 
overcomplicate things. 
Sometimes all you need to do is to pay attention at the error and take it from there.














