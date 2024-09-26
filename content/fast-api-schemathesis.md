title: Test FastAPI apis with Schemathesis
date: 2024-09-20
author: Adriana Vasiu
category: testing




poetry add "fastapi[standard]" sqlalchemy

poetry add schemathesis



INitial code:

        tutorial = Tutorial(
            **tutorial_data.dict()
        )
        db.add(tutorial)
        db.commit()


First fix:

Pydantic model

Route:

    try:
        tutorial = Tutorial(
            **tutorial_data.dict()
        )
        db.add(tutorial)
        db.commit()
    except exc.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="A tutorial with this title already exists",
        )


Error 1


sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: tutorial.category
[SQL: INSERT INTO tutorial (topic, category, author) VALUES (?, ?, ?)]


Error 2

sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: tutorial.topic
[SQL: INSERT INTO tutorial (topic, category, author) VALUES (?, ?, ?)]




poetry run st run http://127.0.0.1:8000/openapi.json --experimental=openapi-3.1  -c all


Curl example to reproduce the error: 

curl -X POST -H 'Content-Type: application/json' -d '{"author": "", "category": "", "title": ""}' http://127.0.0.1:8000/tutorials/

```shell
______________________________________________________________________________________________________________ POST /tutorials/ ______________________________________________________________________________________________________________
1. Test Case ID: s34vdr

- Server error

- Undocumented HTTP status code

    Received: 500
    Documented: 200, 422

[500] Internal Server Error:

    `Internal Server Error`

Reproduce with:

    curl -X POST -H 'Content-Type: application/json' -d '{"author": "", "category": null, "topic": ""}' http://127.0.0.1:8000/tutorials/

================================================================================================================== SUMMARY ===================================================================================================================

Performed checks:
    not_a_server_error                              0 / 9 passed          FAILED
    status_code_conformance                         0 / 9 passed          FAILED
    content_type_conformance                        9 / 9 passed          PASSED
    response_headers_conformance                    9 / 9 passed          PASSED
    response_schema_conformance                     9 / 9 passed          PASSED
    negative_data_rejection                         9 / 9 passed          PASSED
    ignored_auth                                    9 / 9 passed          PASSED
```

Second result


```shell
______________________________________________________________________________________________________________ POST /tutorials/ ______________________________________________________________________________________________________________
1. Test Case ID: kuz17U

- Undocumented HTTP status code

    Received: 409
    Documented: 200, 422

[409] Conflict:

    `{"detail":"A tutorial with this topic already exists"}`

Reproduce with:

    curl -X POST -H 'Content-Type: application/json' -d '{"author": "", "category": "", "topic": ""}' http://127.0.0.1:8000/tutorials/

================================================================================================================== SUMMARY ===================================================================================================================

Performed checks:
    not_a_server_error                              5 / 5 passed          PASSED
    status_code_conformance                         0 / 5 passed          FAILED
    content_type_conformance                        5 / 5 passed          PASSED
    response_headers_conformance                    5 / 5 passed          PASSED
    response_schema_conformance                     5 / 5 passed          PASSED
    negative_data_rejection                         5 / 5 passed          PASSED
    ignored_auth                                    5 / 5 passed          PASSED
```


Final result



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



sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: tutorial.title
[SQL: INSERT INTO tutorial (title, category, author) VALUES (?, ?, ?)]



