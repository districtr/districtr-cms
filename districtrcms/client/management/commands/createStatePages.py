import csv
import urllib.request

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from wagtail.core.models import Page

from districtrcms.client.models import MapIndexPage


class Command(BaseCommand):
    help = "Creates a page for each state."

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete", action="store_true", help="Delete existing state pages."
        )

    def handle(self, *args, **options):

        parent_page = Page.objects.get(title="States").specific

        url = "https://www2.census.gov/geo/docs/reference/state.txt"
        response = urllib.request.urlopen(url)
        statereader = csv.reader(
            response.read().decode("utf-8").splitlines(), delimiter="|"
        )

        next(statereader)
        for row in statereader:
            # id=(int(row[0]))
            # fips=str(row[0])
            name = str(row[2])
            slug = slugify(str(row[2])[:30])
            # abbr=str(row[1])

            try:
                state_page = MapIndexPage.objects.get(title=name).specific
                self.stdout.write(self.style.NOTICE(f"** State Page Found: {name}"))

            except ObjectDoesNotExist:
                state_page = MapIndexPage(title=name, slug=slug)
                parent_page.add_child(instance=state_page)
                state_page.save()
                self.stdout.write(self.style.SUCCESS(f"* State Page Created: {name}"))
