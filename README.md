# Leth
Leth is an experimental feed reader and reading list handler.
Think of it as a mix between _pocket_ and _feedly_.

## Status
Leth is alpha software, it may not work properly or not work at all.
It may even eat your dog.

There is currently no client or publicly running instance.
We are not yet ready for dogfooding ourselves.

## Requirements
Leth is written in python using [Django](https://www.djangoproject.com/) framework.
See the [requirements file](src/requirements.txt) to get an accurate list of dependencies.

## Running Leth
The easiest way to test leth is to use [docker](https://www.docker.com/) and
[docker-compose](https://docs.docker.com/compose/).
Once docker and docker-compose are installed, you are just a few steps away from leth.
In a terminal in project root:

    docker-compose build
    docker-compose start
    docker-compose run app ./manage.py migrate
    docker-compose run app ./manage.py createsuperuser

You should be able to access the API doc on <http://127.0.0.1:8001>.
Log in with your newly created user.

## Roadmap

There is not roadmap yet, our goals are:
* make it possible to store/retrieve feeds (rss/atom)
* make it possible to store/retrive arbitrary page (à la pocket)
* write some tests

Here are features that will be planned once we are out of this _pre alpha_ state:
* clever feed retrieval
* tags and associated filters
* search
* content suggestion
* group sharing?
* your proposition?
