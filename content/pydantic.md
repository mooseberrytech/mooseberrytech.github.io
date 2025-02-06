title: Five things I love about pydantic
date: 2025-02-06
author: Adriana Vasiu
category: development

Whenever I use [pydantic](https://docs.pydantic.dev/latest/) for anything to do with data validation or serialization, I feel like it just works!
It offers so much out of the box and is very intuitive. Is the perfect tool because it allows you to focus on the problem
at hand rather than getting sidetracked into learning some complicated syntax. 

## How to install it

Run `poetry add pydantic` in your poetry project. 

## 1. Out of the box data validation 

Whether you are importing a CSV, a toml file or any data source, pydantic has a lot of out of the box validation ready to use. 

Let's assume that you have the following data in `candidates.csv`:
```shell
name,email,score,exam_date
Bob,bob@email.com,70,2026-01-01
Alice,alice@email.com,78,2024-05-01
```

Here is how you can validate the data with pydantic:

```python
import csv
from pydantic import BaseModel, EmailStr, PositiveInt, FutureDate

class Candidate(BaseModel):
    name: str
    email: EmailStr
    score: PositiveInt
    exam_date: FutureDate

with open('candidates.csv') as f:
    reader = csv.DictReader(f)
    candidates = [Candidate.model_validate(row) for row in reader]
print(candidates)

# pydantic_core._pydantic_core.ValidationError: 1 validation error for Candidate
# exam_date
#  Date should be in the future [type=date_future, input_value='2024-05-01', input_type=str]
```

There are a lot of types that you can enforce on a model, to see all of them you can explore the `pydantic.typing` module in the python REPL:

```shell
>>> from pydantic import types
>>> dir(types)
```

Note: The pydantic email validator is optional, so you need to explicitly install it:

`poetry add 'pydantic[email]'`.

## 2. Managing Settings

This feature requires installing the `pydantic-settings` library:

`poetry add pydantic-settings`

Let's say that you want to define some runtime settings for your functional testing environment in `pydantic_examples.py`:

```python
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class FunctionalTestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    test_url: AnyHttpUrl

if __name__ == "__main__":
    print(FunctionalTestSettings())
```

You can source values from the environment:

```shell
$test_url=http://www.example.com python pydantic_examples.py

#test_url=AnyHttpUrl('http://www.example.com/')
```

## 3. Function arguments validation

```python
from pydantic import PositiveInt, validate_arguments

@validate_arguments
def validate_some_number(positive: PositiveInt):
    print(f"I am doing something important with this number {positive}")

validate_some_number(-9)

# pydantic_core._pydantic_core.ValidationError: 1 validation error for ValidateSomeNumber
# positive
#   Input should be greater than 0 [type=greater_than, input_value=-9, input_type=int]
#
```

## 4. Before and after field validation

Let's assume that you want to build a model that validates a string has a max length and then transform it into uppercase.
But you don't want to worry about some extra spaces, you would rather strip those before the validation kicks in.
With pydantic, you can you the `field_validator` decorator for this:

```python
from pydantic import BaseModel, field_validator, Field

class MyModel(BaseModel):
    my_string: str = Field(max_length=5)

    @field_validator('my_string', mode='before')
    @classmethod
    def ensure_stripped(cls, value: str) -> str:
        return value.strip()

    @field_validator('my_string', mode='after')
    @classmethod
    def ensure_uppercased(cls, value: str) -> str:
        return value.upper()

print(MyModel(my_string="abcd     "))

# ABCD
```

Even if the input string is longer than 5 characters in the example above, we don't reach validation until we 
execute the `field_validator` in `before` mode.

## 5. JSON Schemas 

Pydantic offers a very intuitive interface for dealing with JSON Schemas.

You can create JSON Schemas even from simple types by using the `TypeAdapter`:

```python
from pydantic import TypeAdapter

adapter = TypeAdapter(list[int])
print(adapter.json_schema())

# {'items': {'type': 'integer'}, 'type': 'array'}
```

When you generate a json schema from a model, the default mode is `validation` but you can also use `serialization` mode.
This is depending on if you need a JSON schema required for validating inputs, or one that will be matched by serialization outputs:

```python
from decimal import Decimal
from pydantic import BaseModel

class MyModel(BaseModel):
    my_number: Decimal = Decimal('0.5')

print(MyModel.model_json_schema(mode='validation'))

# {
#   'properties': {
#     'my_number': {
#       'anyOf': [
#         {
#           'type': 'number'
#         },
#         {
#           'type': 'string'
#         }
#       ],
#       'default': '0.5',
#       'title': 'My Number'
#     }
#   },
#   'title': 'MyModel',
#   'type': 'object'
# }

print(MyModel.model_json_schema(mode='serialization'))

# {
#   'properties': {
#     'my_number': {
#       'default': '0.5',
#       'title': 'My Number',
#       'type': 'string'
#     }
#   },
#   'title': 'MyModel',
#   'type': 'object'
# }
```

## Summary

There is much more that you can do with `pydantic`, those were just the 5 top things I could think of that you can use 
with very little effort. 
When you start using it in large codebases you can generate OpenApi specs, do custom validators and much more.


