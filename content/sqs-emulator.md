title: Simple python client for a SQS emulator
date: 2025-01-08
author: Adriana Vasiu
category: testing

# Introduction

This is a post about how to write a simple python client for a sqs emulator, for the purpose of functional testing.

## How to run the queue emulator

Pre-requisites:

- `docker`
- `docker-compose`

The easiest way to run a queue emulator in a deployed environment or locally is to use a docker image.
There is a publicly available base image that you can use, you just need to add your configuration of the queues on top of that.

Create a config file called `emulator.conf`:

```shell
include classpath("application.conf")
queues {
  test-queue {
    fifo = true
  }
}
```

Create a `Dockerfile` that adds the config in a location where the emulator can find it:

```dockerfile
FROM softwaremill/elasticmq-native
COPY emulator.conf /opt/elasticmq.conf
```

The emulator will run on port `9324` by default, so you can spin it up with `docker-compose up` using this configuration
in your `docker-compose.yaml` file:

```yaml
services:
  emulator:
    build: emulator
    ports:
      - "9324:9324"
```

## How to create a simple python emulator client

In order to interact with the emulator and test the functionality it supports, you can use a simple python client that looks like this:

```python
import json
import uuid
import boto3


class SqsEmulatorClient:

    def __init__(self):
        self._client = boto3.client(
            "sqs",
            region_name="elasticmq",
            endpoint_url="http://localhost:9324",
            aws_access_key_id="secret-key-id",
            aws_secret_access_key="secret-key",
            use_ssl=False,
        )
        self._queue = "test-queue.fifo"
        self._queue_url = self._get_queue_url(self._queue)

    def send_message(self, content: str) -> str:
        message_data = {
            "content": content,
        }
        message = (
            """{
        "Type": "Notification",
        "MessageId":"""
            + f'"some-message-id"'
            + """,
        "Message": """
            + json.dumps(message_data)
            + """,
        }"""
        )

        response = self._client.send_message(
            QueueUrl=self._queue_url,
            MessageBody=message,
            MessageGroupId=f"{uuid.uuid4()}",
            MessageDeduplicationId=f"{uuid.uuid4()}",
        )
        return response["ResponseMetadata"]["HTTPStatusCode"]

    def read_messages(self):
        messages = self._client.receive_message(
            QueueUrl=self._queue_url,
            WaitTimeSeconds=5,
            MaxNumberOfMessages=10,
            ReceiveRequestAttemptId=str(uuid.uuid4()),
        )
        message_list = messages.get("Messages")
        return message_list

    def delete_message(self, receipt_handle: str):
        self._client.delete_message(QueueUrl=self._queue_url, ReceiptHandle=receipt_handle)

    def purge_queue(self):
        self._client.purge_queue(QueueUrl=self._queue_url)

    def _get_queue_url(self, queue_name: str) -> str:
        return self._client.get_queue_url(QueueName=queue_name)["QueueUrl"]
```

The only pre-requisite for this client is the `boto3` library.
Assuming you are using `poetry` to install dependencies, run:
```shell
poetry add boto3
```

Now you can interact with the emulator using the client above.

Send a message and read it back.

```shell
>>> client = SqsEmulatorClient()
>>> client.send_message("Hello")
200
>>> client.read_messages()
[{'MessageId': '1d2d8ca9-0165-4405-ae05-048a6f4559d8', 'ReceiptHandle': '1d2d8ca9-0165-4405-ae05-048a6f4559d8#df729bbc-706d-4ff7-941f-36f6772aec21', 'MD5OfBody': '4192ab737454363e4a69257e68315cf3', 'Body': '{\n        "Type": "Notification",\n        "MessageId":"some-message-id",\n        "Message": {"content": "Hello"},\n        }'}]
```

Send another messages and read both messages.

```shell
>>> client.send_message("Moose")
200
>>> client.read_messages()
[{'MessageId': 'd1abaa75-5d94-4977-b49a-cbf9a6c8d4d4', 'ReceiptHandle': 'd1abaa75-5d94-4977-b49a-cbf9a6c8d4d4#f15b5809-e792-499f-a74e-087dbb645427', 'MD5OfBody': '41a63a8331c41a520929af9f3575fbc7', 'Body': '{\n        "Type": "Notification",\n        "MessageId":"some-message-id",\n        "Message": {"content": "Moose"},\n        }'}, 
{'MessageId': '1d2d8ca9-0165-4405-ae05-048a6f4559d8', 'ReceiptHandle': '1d2d8ca9-0165-4405-ae05-048a6f4559d8#6c687b57-b751-4fee-b164-8e9abbb22af8', 'MD5OfBody': '4192ab737454363e4a69257e68315cf3', 'Body': '{\n        "Type": "Notification",\n        "MessageId":"some-message-id",\n        "Message": {"content": "Hello"},\n        }'}]
>>>
```

Please note that reading a message does not remove it from the queue, you need to delete it if you want it removed.
In order to remove a message, you need to delete it from the queue using the receipt handle.

```shell
>>> client.delete_message(receipt_handle="d1abaa75-5d94-4977-b49a-cbf9a6c8d4d4#f15b5809-e792-499f-a74e-087dbb645427")
>>> client.read_messages()
[{'MessageId': '1d2d8ca9-0165-4405-ae05-048a6f4559d8', 'ReceiptHandle': '1d2d8ca9-0165-4405-ae05-048a6f4559d8#35c591a7-f3ae-4fd2-96ed-be35e5f14173', 'MD5OfBody': '4192ab737454363e4a69257e68315cf3', 'Body': '{\n        "Type": "Notification",\n        "MessageId":"some-message-id",\n        "Message": {"content": "Hello"},\n        }'}]
>>>
```

You can also purge the entire queue:

```shell
>>> client.purge_queue()
>>>
>>> client.read_messages()
[]
```

## Summary

Emulating a sqs queue for the purpose of testing is a very straight forward task,
and it removes the dependency on a real queue for your testing. 
This also means that your local, ci and deployed testing can use the exact same mechanism for validating your code. 










