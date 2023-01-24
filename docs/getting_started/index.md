# Getting Started

```{note}
This project uses Docker and Docker Compose for development and production deployment. You can see Cookiecutter Django's documentation on [Getting Up and Running Locally With Docker](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html) and [Deployment with Docker](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html) for more information on the projects environment.
```

## Quick Start

```bash
$ git clone [this repository]
$ cd districtrcms
$ docker-compose -f local.yml build
$ docker-compose -f local.yml up
```

To run in detached mode:

```bash
$ docker-compose -f local.yml up -d
```

You can omit the config file flag by exporting the location:

```bash
$ export COMPOSE_FILE=local.yml
$ docker-compose up
```

Run commands on containers:

```bash
$ docker-compose run —rm django python manage.py dumpdata
```

Execute commands on containers

```bash
$ docker-compose exec postgres backups
```

## How Districtr CMS works with the Districtr site

Districtr CMS is used to managed data that is sent to the Gatsby build process which creates the new Districtr. Data which is used by the pages is also either stored directly in the CMS or references to the data are stored in their place. Pages on the Districtr site are organized in a tree which reflect the Districtr site map with a few expections.

Live pages in the the CMS will be created at build time by the Districtr client. However, triggering a full site rebuild is not always practical or necessary. When a url route that does not yet exist is visited on the client side, the Districtr site will first check if that page content is available over the API before returning a 404. If it is available it will be used to prepare the page like it would have if found during build time.

```{note}
### Previewing Site Content

For the moment, the CMS will redirect you the API endpoint for the page so that you can view that response rather than a frontend preview of the page. If you are running the mapbox-gl-districtr project or districtr-client then changes to the development environment will be available when the project rebuilds.
```

```{toctree}
---
maxdepth: 2
titlesonly:
---
basic_commands
development
deployment
```
