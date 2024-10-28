title: Instrumentation Essentials - Correlated Logs in Django
date: 2024-10-28
author: Adriana Vasiu
category: instrumentation

### Introduction

This is a post about a simple technique to add a correlation id in the `django` logs, when using `structlog`.

### What do you need to install?

This post is assuming that you have the following already setup:

- [poetry](https://python-poetry.org/) for installing your dependencies
- [django](https://www.djangoproject.com/) as your web framework

Add the following dependencies to your project:

```shell
poetry add django-structlog django-guid
```

### How to configure the logging with correlation id

Both [django-structlog](https://django-structlog.readthedocs.io/en/latest/) and [django-guid](https://django-guid.readthedocs.io/en/latest/)
can be used as [django middlewares](https://docs.djangoproject.com/en/5.1/topics/http/middleware/).
Basically, they hook into the request/response processing.

There are a few things that you need to set up. 

#### 1. Configure your installed apps

In your [django settings](https://docs.djangoproject.com/en/5.1/ref/settings/), update your list of installed apps:

```python
INSTALLED_APPS = [
    # more apps here ...
    "django_structlog",
    "django_guid",
]
```

#### 2. Configure your middlewares

Add the middlewares to your existing middleware configuration:

```python
MIDDLEWARE = [
    # more middlewares here ...
    "django_guid.middleware.guid_middleware",
    "django_structlog.middlewares.RequestMiddleware",
]
```

#### 3. Configure django-guid

Add the following configuration for the `django_guid`:

```python
DJANGO_GUID = {
    "GUID_HEADER_NAME": "X-Correlation-ID", 
    ...
    "INTEGRATIONS": [
        CeleryIntegration(
            use_django_logging=True,
            log_parent=True,
        )
    ],
}
```

Those are some basic settings for the `django-guid` library. Things to note here:

- when set in a request, the `X-Correlation-ID` header will be used to set a `guid` in the context of that request
- the library supports passing the `guid` that exists in the context to a celery task and celery sub-task

With these sort of settings you have the ability to benefit from having a `guid` in the context by simply
setting the `X-Correlation-ID` header. If it's not set, the library will generate a `guid` for you. 

#### 4. Setup your logging with django-structlog

At the very minimum, you will have something like this in your settings:

```python
import structlog

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        # let's assume you want your logs to be in json
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
    },
    "handlers": {
        # just a console handler for now
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json_formatter",
        },
    },
    "loggers": {
        # you will most likely have more loggers here
        "django_structlog": {
            "level": "INFO",
        },
    },
}
```

You will also have some `structlog` processors configured:

```python
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        # loads more processors here, whatever you choose to expose in logs
    ],
    ...
)
```

#### 5. Create a structlog processor and update your structlog processor list

So you have a basic logging and structlog configuration above, and you have the ability to set a `guid` in the context of 
your requests that gets passed down to celery tasks for example, or other requests. 

Let's expose this in the logs by creating a processor and adding it to your list.

Create a simple processor:

```python
from django_guid import get_guid
def add_correlation_id_processor(logger: logging.Logger, method_name, event_dict):
    # Adds the contextual guid populated by the django-guid into your json log
    event_dict["correlation_id"] = get_guid()

    return event_dict
```

Add the processor to your list of processors in your django settings:

```python
structlog.configure(
    processors=[
        ...
        add_correlation_id_processor,
        ...
    ],
    ...
)
```

And that's it! Next time you do a request  with the `X-Correlation-ID` header set, the `correlation_id` will appear in your logs. 
Your request log for example will look something like this:

```json
{
    "request": "GET some/url",
    "correlation_id": "<some-guid-you-generated>",
    ...
}
```

Any logs you will generate in the context of that request, including any celery logs for tasks you will invoke, will contain 
the `correlation_id`. 
If for some reason you need to reset the correlation id, just use the `django_guid.set_guid` functionality, this will 
reset the context and the following log statements in that context will be updated.

### Summary

By using `django-structlog` processors in combination with the contextual `guid` that can retrieved using `django-guid.get_guid`
you can easily add a correlation id that can be very useful, especially when you want to track an entire process, that
might include celery tasks. 







