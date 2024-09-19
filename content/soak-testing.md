title: What is Soak Testing?
date: 2024-09-19
author: Adriana Vasiu
category: testing


### Introduction

This post is aiming to give you some guidance on when to do soak testing, how to achieve it and how to measure the test results.

### What is Soak Testing?

When I explain soak testing I like to start with this metaphor: 
"Imagine that you have a product that has to be water-resistant, and you want to test it. 
It's not enough to splash it with water from time to time, you actually need to soak it for a while and see what is happening to it. 
Does it expand? Does it disintegrate?"

In software, soak testing means you expose your application to production-like load under a prolonged period of time, 
so you can see the effects on your system. 

### What do you aim to uncover with soak testing? 

Let's assume that you have a system with the following characteristics:

- it exposes some APIs 
- it connects to a database
- it calls external systems 
- it runs some tasks in the background 
  - some tasks access the database
  - some tasks are long-run

Let's assume that you have a soak test that runs for a few hours and does the following:

- puts load on your APIs
- triggers the tasks that are run in the background
- emulates the external systems

What you want to assess are the following metrics: 

- CPU and memory of services
- database metrics - CPU, memory, number of read/write operations, number of new connections
- task metrics - how long they are running for, what is the size of the queue for the tasks 
- api metrics - response times, error rates

You are looking for memory leaks, growing number of connections, bottlenecks in your systems.

A technique on assessing the metrics will be covered in the section below. 

### Techniques

The following techniques, regardless of how you decide to achieve them, work well in practice.

#### 1. Create an isolated environment

In order to assess the behaviour of the system under test you will need to isolate it from external factors.

**Infrastructure level isolation**

Regardless what infrastructure you use make sure that:

- you allocate enough CPU and memory
- other service runtimes cannot affect your test run

**Logical isolation**

Emulate any external dependencies that you have. Create mock servers where you can simulate appropriate delays
depending on the SLAs you are expecting from your dependencies.
This way you will build a deterministic test. 

#### 2. Build flexible test profiles

**Consider a data-driven profile**

The most extensible test profiles I used are data driven. 
For example, if you want to include a new API in your test, add the new API to the profile and the test will pick it up. 
You could write custom code to load the profile and generate the test code by using a templating mechanism.
Your profile could be yaml, json, or whatever other form of configuration your prefer.

**Consider how users exercise your system**

When putting together the profile you need to consider how users are accessing your system. 
Those users can be end users but for back-end systems most likely those users would be other services. 
Are those services in the same cluster and can access your own service via an internal service discovery mechanism?
Or are they outside your own ecosystem? This will influence the test because you might want to test via a load balancer for 
example.


#### 2. Have configurable and stackable tests 

When you have multiple parts of the systems that you are trying to exercise, for example the background tasks as well 
as some APIs, consider building your tests so that you can exercise the APIs and the tasks separately. 
This gives you more flexibility when you are trying to simulate various profiles like peak and average load lets say. 
You could have a test that runs on constant load to trigger the background tasks and in the same time overlap 
it with tests at various intensity for your APIs.

One simple way to do this would be to build a test image that you use in two separate modes - api testing and task testing.
Then you can run this image in two separate modes using two different jobs.
 
#### 3. Use alerting as an evaluation mechanism 

Let's assume that the aspects of your system that you want to assess after the test are more involved than just response
times for your APIs. 
You want to assess some of the metrics I mentioned in one of the sections above: CPU, memory, DB Metrics etc.

You could look at a dashboard but if you want to assess the results automatically and have a view on how the system
is doing against your production requirements than you can define the alerting on the metrics that you want to assess 
and query the alert data for firing alerts. A lot of the alerting systems have an API for you to do that and I 
included some examples in the tools section below.  

### Tools

Here are some of the tools that I tried in the past and worked well for me:

- [locust](https://locust.io/) for writing tests
- [kubernetes jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) for running different profiles
- [terraform](https://www.terraform.io/) for provisioning the test infrastructure (easy to spin down the infrastructure as well)
- [grafana API](https://grafana.com/docs/grafana/latest/developers/http_api/alerting_provisioning/)
- [alertmanager API](https://github.com/prometheus/alertmanager?tab=readme-ov-file#api)
