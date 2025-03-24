# Reading List Application

## Introduction

This repository contains a small app to manage and track reading. The application provides functionalities to add and search books in a PostgreSQL database.

## Prerequisites

To add pre-commit hooks, run the following command:
```sh
pre-commit install
```

Create a .env similar to .env example and update

You'll need a populated database.
Place a db.sql file within the main directory and update and uncomment db volume in compose.yml
to have the container automatically initialize a databse

## Repository structure

The following are important files and folders in the repository:

* `requirements.txt`: This file contains the Python dependencies needed for the application. These dependencies are automatically installed when you run `docker-compose build`.
* `app.py`: This is the application entry point. It deals with parsing command line parameters and then passing control off to the appropriate module.
* `util/`: This folder contains utility modules, including `database.py` which handles database interactions.

## Running the app
To run the application:
```console
podman-compose up
```
You should be able to access the app at <http://0.0.0.0:8501>
