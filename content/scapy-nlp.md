title: Taking a glance at SpaCy for Natural Processing Language
date: 2025-01-24
author: Adriana Vasiu
category: development

# Introduction

[SpaCy](https://spacy.io/) is an open source library that I haven't tried out before writing this blog post. 
Sometimes is good to look at a tool with beginner's eyes, it's a fair assessment on how easy it is to use.

I do creative writing in my spare time so when I saw that `SpaCy` does [Natural Language Processing](https://en.wikipedia.org/wiki/Natural_language_processing)
I thought it might be useful for analysing my work and getting some insights. 

This post is covering a few of the `SpaCy` features which I found useful. 

## How to install

`SpaCy` can be installed as a python library. Let's assume that we use `poetry` to install our dependencies:

`poetry add spacy`

Note: At the moment `spacy` requires `python <3.13,>=3.9`.

## How to prime

I am going to start with a brief introduction on Natural Language Processing (NLP) because it's useful in this context.
NLP is a subfield of Artificial Intelligence and involves analysing and understanding natural language. The aim for it
is to produce insights based on patterns. 

Some examples of insights that NLP can produce are:

- [Automatic Summarization](https://en.wikipedia.org/wiki/Automatic_summarization)
- [Named-entity Recognition](https://en.wikipedia.org/wiki/Named-entity_recognition)
- [Sentiment Analysis](https://en.wikipedia.org/wiki/Sentiment_analysis)


The insights for NLP work on models. For example, there are different models for different languages. 
For this post I used the `en_core_web_sm` model, which is the default model for English at this point in time.

Download the model:

```poetry run python -m spacy download en_core_web_sm```

Note: If you use a system-wide `python` installation, or if you are in an activated virtual environment, you can 
just run: `python -m spacy download en_core_web_sm`

We should get an output like this which prompts us to do the next step:

```shell
✔ Download and installation successful
You can now load the package via spacy.load('en_core_web_sm')
```

Let's load the model into the library from the python REPL (python interpreter):

```shell
>>>
>>> import spacy
>>> nlp = spacy.load("en_core_web_sm")
>>>
```

Done. Now we are ready to explore the `spacy` features. 

## How to start processing text 

So what is the `nlp` object that we just constructed above? Let's explore it in REPL:

```shell
>>> nlp
<spacy.lang.en.English object at 0x116a058b0>
>>>
>>> help(nlp)
```

A snippet of the output returned by the `help` command looks like this:

```shell
Help on English in module spacy.lang.en object:

class English(spacy.language.Language)
...
Methods inherited from spacy.language.Language:
...
 |  __call__(self, text: Union[str, spacy.tokens.doc.Doc], *, disable: Iterable[str] = [], component_cfg: Optional[Dict[str, Dict[str, Any]]] = None) -> spacy.tokens.doc.Doc
 |      Apply the pipeline to some text. The text can span multiple sentences,
 |      and can contain arbitrary whitespace. Alignment into the original string
 |      is preserved.
 |      ...
 |      RETURNS (Doc): A container for accessing the annotations.
 |
 |      DOCS: https://spacy.io/api/language#call
```

So at this point, even by skimming through the help provided on this object, we can make out that is callable, and it accepts some text.
So let's call and see what we get:

```shell
>>>blog_doc = nlp("This is a post about the spacy library usage. Let's analyse the text in the post.")
>>>
>>> type(blog_doc)
<class 'spacy.tokens.doc.Doc'>
```

So we get a [Doc](https://spacy.io/api/doc) object. What can we do with it?

```shell
>>>help(blog_doc)
```

The `help` output gives us further clues:

```shell
Help on Doc object:

class Doc(builtins.object)
 |  Doc(Vocab vocab, words=None, spaces=None, user_data=None, *, tags=None, pos=None, morphs=None, lemmas=None, heads=None, deps=None, sent_starts=None, ents=None)
 |  A sequence of Token objects. Access sentences and named entities, export
 |      annotations to numpy arrays, losslessly serialize to compressed binary
 |      strings. The `Doc` object holds an array of `TokenC` structs. The
 |      Python-level `Token` and `Span` objects are views of this array, i.e.
 |      they don't own the data themselves.
 |
 |      EXAMPLE:
 |          Construction 1
 |          >>> doc = nlp(u'Some text')
 |
 |          Construction 2
 |          >>> from spacy.tokens import Doc
 |          >>> doc = Doc(nlp.vocab, words=["hello", "world", "!"], spaces=[True, False, False])
 |
 |      DOCS: https://spacy.io/api/doc
```

Ok, so the Doc object contains a series of tokens, let's explore that:

```shell
>>> [token.text for token in blog_doc]
['This', 'is', 'a', 'post', 'about', 'the', 'spacy', 'library', 'usage', '.', 'Let', "'s", 'analyse', 'the', 'text', 'in', 'the', 'post', '.']
```

So just as easy as this, we can split the text into words and punctuation marks.
What useful operations can we do on these tokens? 

Let's say we want to:

- count the frequency of the words, to see how much we are repeating ourselves
- filter out the punctuation
- count the number of sentences

If we explore a token object, we get more information about what we can do with it:

```shell
>>>dir(blog_doc[0])
[ ...'is_alpha', ...'is_digit', ... 'is_punct'...'is_stop'...]
```

There is a lot more functionality that the tokens offer, I just picked a few methods. 
Let's count the word frequency:

```shell
>>> words = [
...     token.text for token in blog_doc
...     if not token.is_punct
... ]
>>>
>>> words
['This', 'is', 'a', 'post', 'about', 'the', 'spacy', 'library', 'usage', 'Let', "'s", 'analyse', 'the', 'text', 'in', 'the', 'post']
>>>
>>> from collections import Counter
>>> print(Counter(words).most_common(2))
[('the', 3), ('post', 2)]
>>>
```

When we do analysis on large texts we probably want to remove the words that are necessary in order for the sentences to make
sense from a grammatical point of view, but they are not significant. Those words are called "stop words" in NLP. 
A few examples in English would be: but, and, then, the.

```shell
>>> words = [
...     token.text for token in blog_doc
...     if not token.is_stop is not token.is_punct
... ]
>>> words
['post', 'spacy', 'library', 'usage', 'Let', 'analyse', 'text', 'post']
>>>
```

Now let's look at sentences:

```shell
>>>
>>> sentences = list(blog_doc.sents)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "spacy/tokens/doc.pyx", line 926, in sents
ValueError: [E030] Sentence boundaries unset. You can add the 'sentencizer' component to the pipeline with: `nlp.add_pipe('sentencizer')`. Alternatively, add the dependency parser or sentence recognizer, or set sentence boundaries by setting `doc[i].is_sent_start`.
```
 
Ok, so this doesn't work out of the box but the instructions are pretty clear:

```shell
>>> nlp.add_pipe('sentencizer')
>>> blog_doc = nlp("This is a post about the spacy library usage. Let's analyse the text in the post.")
>>> sentences = blog_doc.sents
>>> [sentence for sentence in sentences]
[This is a post about the spacy library usage., Let's analyse the text in the post.]
```

Note: We need to make sure we call again the nlp Language object with our text in order for the [sentence recognizer](https://spacy.io/api/sentencerecognizer) to be applied.

# Further thoughts

- exploring a library step by step, by using the python REPL, is a very quick way to discover the library capabilities
- `SpaCy` has a lot of dependencies, so you need to be aware of that if you want to package it and deploy it
- `Spacy` has a lot more functionality. Here are some of the things it can do:
    - [Part-of-Speech Tagging](https://spacy.io/api/tagger)
    - [Lemmatization](https://spacy.io/api/lemmatizer)
    - [Sentiment Analysis](https://spacy.io/api/large-language-models#sentiment)





