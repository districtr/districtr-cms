# Districtr CMS

Wagtail CMS and API for the Districtr Site

License: MIT

## Introduction

Districtr is the open-source web app that empowers all people to draw districting plans. This is the Wagtail CMS and API that manage the pages and data on the Districtr site.

### Related Districtr Projects

This platform is part of a suite of programs that create Districtr.org.

- mapbox-gl-districtr: A Mapbox extension and tool library for drawing districting plans.
- districtr-client: The Districtr site built on Gatsby
- Other Districtr and MGGG data tools

## Getting Started

### Docker

This project uses Docker and Docker Compose for development and production deployment. You can see Cookiecutter Django's documentation on [Getting Up and Running Locally With Docker](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html) and [Deployment with Docker](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html) for more information on the projects environment.

### Quick Start

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

### Documentation

This app will serve documentation over locahost:9000. To start it in development you must run the up command with the docs profile.

```bash
$ docker-compose --profile include-docs up
```

## Contributing

This suite is under active development and will eventually replace the existing Districtr repository behind Districtr.org.

You can develop this project independently or along with other Districtr projects. If you are interested in contributing, thank you! You can visit the Github Project for the Districtr Reboot and see if there any of our open issues or milestones that you feel you could help with. You can also send an email to engineering@mggg.org to learn more about opportunities with Districtr and MGGG.
