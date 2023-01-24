## Development

### API docs, CMS and User authentication endpoints

- /api/docs/ - Swagger Docs for API
- /wagtail-api/pages - Wagtail pages
- /wagtail-api/documents - Wagtail documents
- /wagtail-api/images - Wagtail images
- /auth-token/

### Sphinx Docs

This app will serve documentation over port 9000. To start it in development you must run the up command with the docs profile.

```bash
$ docker-compose --profile include-docs up
```

### Type checks

Running type checks with mypy:

```
$ docker-compose run --rm django mypy districtrcms
```

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

```
$ docker-compose run --rm django coverage run -m pytest
$ docker-compose run --rm django coverage html
$ docker-compose run --rm django open htmlcov/index.html
```

#### Running tests with pytest

```
$ pytest
```

### Live reloading and Sass CSS compilation

```{warning}
Live reloading is available at localhost:3000. The site will have a limited front-end framework outside of the admin area. The exiting bootstrap placeholder will be completely replaced so develop with it sparingly for now.
```

### Celery

This app comes with Celery. To start it in development you must run the up command with the celery profile.

```bash
$ docker-compose --profile include-celery up
```

To run a celery worker:

```bash
cd districtrcms
celery -A config.celery_app worker -l info
```

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [MailHog](https://github.com/mailhog/MailHog) with a web interface is available as docker container.

With MailHog running, to view messages that are sent by your the CMS, open your browser and go to `http://127.0.0.1:8025`
