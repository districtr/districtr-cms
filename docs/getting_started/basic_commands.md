# Basic Commands

## Setting Up Users

- To create a _superuser account_, use this command:

```
    $ docker-compose run --rm django python manage.py createsuperuser
```

- To create a _normal user account_, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

## Load and Save Test Data

A fixture containing all U.S. States and Counties with the existing Districtr problems and Mapbox sources is availble for development use.

### Dump Data

```bash
$ docker-compose run --rm django python manage.py dumpdata --natural-foreign --indent 2 \
-e contenttypes -e auth.permission -e users.user \
-e wagtailcore.groupcollectionpermission \
-e wagtailcore.grouppagepermission -e wagtailimages.rendition \
-e wagtailcore.revision \
-e sessions > districtrcms/client/fixtures/data.json
```

### Load Test Data

```bash
$ docker-compose run --rm django python manage.py loaddata districtrcms/client/fixtures/data.json
```
