import csv

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

        # Use os to get a path to the directory where this script is located
        import os

        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(dir_path)

        # join the dir_path with the path to the data directory
        data_dir = os.path.join(dir_path, "../data")

        # join the data_dir with the path to the county-page-data.csv file
        county_page_data_file = os.path.join(data_dir, "county-page-data.csv")

        # Get a file called county-page-data.csv from directory where this script is located
        with open(county_page_data_file) as csvfile:

            # Create a reader object
            countyreader = csv.reader(csvfile, delimiter=",")

            # Skip the header row
            next(countyreader)

            # Loop through the rows in the csv file
            for row in countyreader:

                # Get the state name from the csv file
                state_name = str(row[9])

                # Get the state slug from the csv file
                state_slug = slugify(state_name)

                # Get the county name from the csv file
                county_name = str(row[5])

                # Get the county slug from the csv file
                county_slug = slugify(str(row[4]))

                # Print a message to the console
                self.stdout.write(self.style.NOTICE(f"** County Name: {county_name}"))

                # Print a message to the console
                self.stdout.write(self.style.NOTICE(f"** County Slug: {county_slug}"))

                # Print a message to the console
                self.stdout.write(self.style.NOTICE(f"** State Name: {state_name}"))

                # Print a message to the console
                self.stdout.write(self.style.NOTICE(f"** State Slug: {state_slug}"))

                if state_slug == "united-states-virgin-islands":
                    state_slug = "us-virgin-islands"

                if state_slug == "commonwealth-of-the-northern-mariana-islands":
                    state_slug = "northern-mariana-islands"

                states_index_page = Page.objects.get(title="States").specific

                # Get the state page
                state_page = (
                    MapIndexPage.objects.child_of(states_index_page)
                    .get(slug=state_slug)
                    .specific
                )

                self.stdout.write(
                    self.style.NOTICE(f"** State Page Found: {state_page}")
                )

                # Check if a county page already exists as a child of the state_page
                if (
                    MapIndexPage.objects.child_of(state_page)
                    .filter(slug=county_slug)
                    .exists()
                ):
                    # If the county page already exists, print a message to the console
                    self.stdout.write(
                        self.style.NOTICE(f"** County Page Found: {county_name}")
                    )
                    # objs = MapIndexPage.objects.child_of(state_page).filter(slug=county_slug)

                    # objs.delete()

                    continue

                else:
                    # If the county page does not exist, print a message to the console
                    self.stdout.write(
                        self.style.NOTICE(f"** County Page Not Found: {county_name}")
                    )

                # Create a county page
                county_page = MapIndexPage(title=county_name, slug=county_slug)

                self.stdout.write(
                    self.style.NOTICE(f"** County Page Created: {county_page}")
                )

                self.stdout.write(
                    self.style.NOTICE(f"** State Page Found: {state_page}")
                )

                # Add the county page to the state page
                state_page.add_child(instance=county_page)

                # Save the county page
                county_page.save()

                # Print a message to the console
                self.stdout.write(
                    self.style.SUCCESS(f"* County Page Created: {county_name}")
                )
