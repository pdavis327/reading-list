# [TODO]: Write your repository name here, like `Example pipeline`

## Introduction

[TODO]: Write an introduction to what your pipeline is supposed to do, at a high level, in one sentence.

## Prerequisites

To add pre-commit hooks, run the following command:
`pre-commit install`

## Repository structure
[TODO: Update this as needed]

The following are important files and folders in the repository:

* `requirements.txt`: Like for any standard python package, this file contains any python dependencies you need installed in your docker container for your pipeline to work. These dependencies are automatically installed when you run `docker-compose build`.
* `main.py`: This is the application entry point.   This mostly just deals with parsing command line parameters and then passing control off to pipeline.py
* `pipeline.py`: This is where the work is done. See the example pipeline code as a guide for how to structure this
* `util/`: This folder contains some utility modules.
* `assets/`: This folder contains data files such as jinja2 templated sql queries and json-formatted bigquery schema files

## Running locally
[TODO: Replace this as needed]
This template comes with a fully functional example pipeline which should run for you if everything is configured correctly.

You can run the pipeline from within docker (which is how it will run when automated), or you can run it locally on your machine

### Running within docker
To run in docker, first build the docker image.
This will happen automatically the first time you run the pipeline.
To display the command line parameters:
```console
docker compose run --rm pipeline --help
```

You can also build the image with the build.sh
which will add some git environmental variables

```console
bash build.sh
```

To run the example:
```console
docker compose run --rm pipeline \
training \
--source_training_data=assets/iris.csv
```

For pipelines with multiple operations
you can use the run.sh to chain the commands

```console
bash run.sh
```
### Running from your local python environment

You can also run and test using your local python environment.

To setup your local python environment
```console
conda activate venv
pip install -r requirements.txt
```

Then to run the pipeline
```console
python main.py --help
```
or
```console
python main.py training  --source_training_data=/assets/iris.csv
```

For convenience, there are some shell scripts for building and running using `docker compose`
+ `build.sh`    This will run `docker compose build` and pass in some extra info on the current git commit
+ `run.sh`      This will run the pipeline using `docker compose run`.  Edit the file to set the parameters you want to use
+ `cloud-build.sh` This will do a manual cloud build and publish the docker container to the cloud registry
