title: Verify your APIs against the OpenAPI spec with Schemathesis
date: 2024-09-28
author: Adriana Vasiu
category: testing

### Introduction

This post is about improving the quality of your APIs by verifying if they match the [OpenAPI](https://www.openapis.org/) spec. 

### Why Schemathesis?

I have been using [OpenAPI](https://www.openapis.org/) specs for all the projects I worked on recently.
I discovered that using an auto generated spec doesn't always guarantee that:

- you have documented all the outputs for your API
- you have handled all the edge cases correctly

You can rely on the schemas that your framework provides to do data validation.
But that doesn't mean you have captured all the rules correctly before your data ends up in the db layer. 
There is an element of human error when making those layers work together.

I have been using the [hypothesis](https://hypothesis.readthedocs.io/en/latest/) python testing library in the past.
`Hypothesis` does property based testing by generating arbitrary data that matches the specification of your code 
and asserting your code works correctly in all cases, not only the cases that you think about. 

The first thing that came into my mind when I thought about validating APIs was to use the same concept, but with the `OpenAPI` spec as my input. 
I wanted my spec to be the blueprint for generating test cases automatically.

That led me straight to [schemathesis](https://schemathesis.readthedocs.io/en/stable/).

### How to use Schemathesis with FastAPI

If you haven't used [FastAPI](https://fastapi.tiangolo.com/), have a look at the documentation, is very easy to setup 
with a database. For development and learning is easiest if you use a db like [sqlite](https://www.sqlite.org/).

If you want to see the full example I used for this blog post have a look [here](https://github.com/mooseberrytech/fast-api-playground).

#### Prerequisites

You have a database model, a [pydantic](https://docs.pydantic.dev/latest/) schema and a route:

```python
# Initial code
class Tutorial(Base):
    """Model"""
    __tablename__ = "tutorial"
    id = Column(Integer, primary_key=True)
    topic = Column(String(50), nullable=False, unique=True)
    category = Column(String, nullable=False)
    author = Column(String, nullable=False)

class TutorialCreate(BaseModel):
    """Pydantic Schema"""
    topic: str = Field(max_length=50)
    category: Optional[str]
    author: str

@router.post("/tutorials/")
def create_tutorial(tutorial_data: TutorialCreate, db: Session = Depends(get_db)):
    """Route"""
    tutorial = Tutorial(**tutorial_data.dict())
    db.add(tutorial)
    db.commit()
```

#### Install Schemathesis

Let's assume that you are using [poetry](https://python-poetry.org/) to install your python dependencies:

`poetry add schemathesis`

#### Run schemathesis

It requires a running server:
`poetry run fastapi dev src/main.py`

You can run `schemathesis` either from command line or using `pytest`. I prefer to run via command line because
I find the output more useful but if you want to customise test cases `pytest` is a better approach.

**Command line**

`poetry run schemathesis run http://127.0.0.1:8000/openapi.json --experimental=openapi-3.1  -c all`

`FastApi` exposes the spec on the root url, so you can use that as input for your test. 

**With pytest**

Assuming you have installed `pytest` with `poetry add pytest`, you can start with a very simple test:

```python
import schemathesis

schemathesis.experimental.OPEN_API_3_1.enable()
schema = schemathesis.from_uri("http://127.0.0.1:8000/openapi.json")

@schema.parametrize()
def test_api(case):
    case.call_and_validate()
```

And to run it, use the `pytest` runner:

`poetry run pytest`

#### Analyse the results

With the initial code, when running via command line, you get the following results:

```shell
______________________________________________________________________________________________________________ POST /tutorials/ 
1. Test Case ID: s34vdr
- Server error
- Undocumented HTTP status code
    Received: 500
    Documented: 200, 422
[500] Internal Server Error:
    `Internal Server Error`
Reproduce with:
    curl -X POST -H 'Content-Type: application/json' -d '{"author": "", "category": null, "topic": ""}' http://127.0.0.1:8000/tutorials/
================================================================================================================== SUMMARY
Performed checks:
    not_a_server_error                              0 / 9 passed          FAILED
    status_code_conformance                         0 / 9 passed          FAILED
    content_type_conformance                        9 / 9 passed          PASSED
    response_headers_conformance                    9 / 9 passed          PASSED
    response_schema_conformance                     9 / 9 passed          PASSED
    negative_data_rejection                         9 / 9 passed          PASSED
    ignored_auth                                    9 / 9 passed          PASSED
```

So at this point you know that the test uncovered some `500` errors. Something is not handled as expected.
`Schemathesis` even offers you a curl command to reproduce the errors and the server logs will give you more information:
```shell
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: tutorial.category
[SQL: INSERT INTO tutorial (topic, category, author) VALUES (?, ?, ?)]

sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: tutorial.topic
[SQL: INSERT INTO tutorial (topic, category, author) VALUES (?, ?, ?)]
```
At this point you know that you haven't handled correctly the `category` being mandatory, and the unicity of the `topic`.

A quick fix could look like this:

```python
# Handle the mandatory data in your pydantic schema
# Pydantic validators will issue a 422 if the schema is not respected
class TutorialCreate(BaseModel):
    topic: str = Field(max_length=50)
    category: str
    author: str
    
# Handle the database error in the route
@router.post("/tutorials/")
def create_tutorial(tutorial_data: TutorialCreate, db: Session = Depends(get_db)):
    try:
        tutorial = Tutorial(**tutorial_data.dict())
        db.add(tutorial)
        db.commit()
    except exc.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="A tutorial with this topic already exists",
        )
```

Re-running `schemathesis` will now produce this:

```shell
______________________________________________________________________________________________________________ POST /tutorials/ _____
1. Test Case ID: kuz17U
- Undocumented HTTP status code
    Received: 409
    Documented: 200, 422
[409] Conflict:
    `{"detail":"A tutorial with this topic already exists"}`
Reproduce with:
    curl -X POST -H 'Content-Type: application/json' -d '{"author": "", "category": "", "topic": ""}' http://127.0.0.1:8000/tutorials/
================================================================================================================== SUMMARY ==========
Performed checks:
    not_a_server_error                              5 / 5 passed          PASSED
    status_code_conformance                         0 / 5 passed          FAILED
    content_type_conformance                        5 / 5 passed          PASSED
    response_headers_conformance                    5 / 5 passed          PASSED
    response_schema_conformance                     5 / 5 passed          PASSED
    negative_data_rejection                         5 / 5 passed          PASSED
    ignored_auth                                    5 / 5 passed          PASSED
```

More tests are now passing but the report reflects that even if you handled the db integrity error, you haven't documented it.
You can add a response code to your route like this:
```python
class Error(BaseModel):
    detail: str

# Response code is included in the decorator
@router.post("/tutorials/", responses={409: {"model": Error}})
def create_tutorial(tutorial_data: TutorialCreate, db: Session = Depends(get_db)):
    try:
        tutorial = Tutorial(**tutorial_data.dict())
        db.add(tutorial)
        db.commit()
    except exc.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="A tutorial with this topic already exists",
        )
```

After a re-run, all test cases should pass. By default, `schemathesis` generates 100 test cases, but you can adjust that.

```shell
POST /tutorials/ .                                                                                                                                                                                    
Performed checks:
    not_a_server_error                              100 / 100 passed          PASSED
    status_code_conformance                         100 / 100 passed          PASSED
    content_type_conformance                        100 / 100 passed          PASSED
    response_headers_conformance                    100 / 100 passed          PASSED
    response_schema_conformance                     100 / 100 passed          PASSED
    negative_data_rejection                         100 / 100 passed          PASSED
    ignored_auth                                    100 / 100 passed          PASSED
```

That's it! On a very simple example, you have already improved your data validation and documented new error codes.

### Limitations

Just from the first few tries of the library, I noticed a few limitations:

- supporting `openapi 3.1` is still an experimental feature, which you have to enable
- when running the tests via `pytest` the summary of the performed checks cannot be enabled. You can set the verbosity of 
  hypothesis but that displays all tests cases and I find it a bit too verbose. 

### Summary

If you are looking for a tool that does schema validation tests than `schemathesis` is very easy to integrate
into your development lifecycle. 

It won't replace unit, integration or functional testing, but it's a great addition to your testing strategy 
when you use `OpenApi` specs. 

If you are confident that your API does what the spec says, in terms of the shape of the data, then your clients 
can confidently generate their mocks based on the spec.
