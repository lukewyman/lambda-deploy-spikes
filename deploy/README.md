# Lambda Deploy Spikes

This repository is a collection of small spike projects to explore various approaches for deploying AWS Lambdas written in Python. The motivation for this effort is a problem I am having with testing, packaging and deployment of Lambdas in my [karaoke-backend-sst](https://github.com/lukewyman/karaoke-backend-sst) project. The project uses [Serverless Stack (sst)](https://serverless-stack.com/) as a framework for a microservices monorepo with API Gateway, Lambda, DynamoDB, and other AWS services, and is written in Python. 


## The Problem

The problem is getting unit testable code to package and deploy:
- I like to create my Lambdas with composable, unit-testable pieces, such as separate data access functions and domain objects. I also like to keep my unit tests separate from my application code.
- If I make the code I want to unit test packageable with a `setup.cfg` and do a `pip install -e .`, this ends up being effective for my unit tests to be able see the functions and classes they are testing, so that works well.
- But then, the Lambda functions have an issue. If I reference my package with `import` statements in the Lambdas, it works fine in Visual Studio Code, but then, once it's deployed, the Lambdas fail because they can't find the package. It's clear the Lambdas would want the packaged code to be installed with pip so they it is accessible to them in their cloud environment.
- The Karaoke application is currently deployable and working, but not as an elegant solution. The way I have this working at the moment, is to keep my testable code in the same folder as the Lambda functions, and then creating a local, editable package out of all of that. This allows the unit tests to see the functions and classes when the tests are run, while also allowing sst to package Lambdas and related testable code together during deployment.


## The Target Solution

What I'd like to achieve, is testable code that is kept separate from my Lambdas such that:
- The testable Python code is locally installable in editable form (with `pip install -e .`) so that both the Lambdas and unit tests can reference it as it changes during development.
- During deployment, the testable Python code is packaged as wheel (`.whl`) file which is included in the deployment of each Lambda.
- This should be possible in either a zip file or container (Docker image) deploment. In the case of zip file deployment, the wheel file would be decompressed and packaged into the zip file. For a container deployment, the wheel file would be copied into the container and installed with a `pip install`.


## The Spikes

These spike projects are designed to start simple and become progressively advanced as they move towards solving the problem. Each spike has its own README with instructions to replicate my results, and summary of the outcome. The first and simplest spikes are simple raw Lambda deployments (without using a serverless framework) that follow the AWS documentation for deploying as a zip file or as a container, etc. The more advanced spikes experiment with packaging separate, testable code into depemdencies that are installed or included with the deployment. <br />
Eventually, the spikes will experiment with using the custom `installCommands` in sst to automate this process. Another possible outcome, is that these concepts are included as an enhancement in future sst releases. <br />
While not part of the original problem, I think that experimenting with Lambda Layers as a part of Lambda deployment would be a natural terminus for this experiment, and I'm looking forward to working on that soon.

### [Spike 1: Deploying a Raw Lambda Without Dependencies as a Zip File](raw-lambda-no-dep-zip/)
The simplest Lambda deployment, no dependencies - a first step.

### [Spike 2: Deploying a Raw Lambda With Dependencies as a Zip File](raw-lambda-with-dep-zip/)
The Lambda in this deployment uses the `requests` library as an example of deploying a Lambda with dependencies.

### [Spike 3: Deploying a Raw Lambda with Dependencies as a Container](raw-lambda-with-dep-image/)
Same as Spike 2, but as a Docker container.

### [Spike 4: Deploying a Lambda Without Dependencies Using SST](sst-lambda-no-dep/)
A simple Lambda, no dependencies. Same as Spike 1, but letting Serverless Stack do the deployment.

### [Spike 5: Deploying a Lambda With Dependencies Using SST](sst-lambda-with-dep)
Again with the `requests` library as a dependency, as in Spike 2, but using Serverless Stack to do the deployment.

### [Spike 6: Deploying a Raw Lambda with Wheel Package as a Container](raw-lambda-whl-package-image/)
Okay, this is where it starts to get interesing. This spike deals with separate, unit-testable code outside of the Lambdas. The non-Lambda code is packaged as a wheel file and copied/installed in the Docker image.

