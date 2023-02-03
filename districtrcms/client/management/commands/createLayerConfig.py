import glob
import json
import os

from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from wagtail.core.blocks.stream_block import StreamValue

from districtrcms.client.models import MapDetailPage, MapIndexPage, Source


class Command(BaseCommand):

    help = "Creates a map detail page for each map."

    def handle(self, *args, **options):
        location = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../data/districtr/assets/data/")
        )

        column_sets = []

        self.stdout.write(self.style.NOTICE(f"Location: {location}"))

        res = f"{location}/*/*.json"

        for file in glob.glob(res):

            self.stdout.write(self.style.NOTICE(f"File: {file}"))

            # parse the json in the file
            with open(file) as f:
                data = json.load(f)

                for item in data:
                    state = item["state"]
                    place_name = item.get("name")
                    if place_name == state:
                        place_name = None

                    if state == "Washington, DC":
                        state = "District of Columbia"

                    for unit in item["units"]:

                        problem_column_sets = unit["columnSets"]
                        problem_geo_key = unit["idColumn"]["key"]

                        if place_name:
                            name = "{} - {} - {}".format(
                                state, place_name, unit["name"]
                            )
                        else:
                            name = "{} - {}".format(state, unit["name"])

                        set = {
                            "id": slugify(name + "-draw"),
                            "key": problem_geo_key,
                            "columnSets": problem_column_sets,
                        }

                        column_sets.append(set)

        # Create a layerConfig.json file and write the column sets to it
        column_sets_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../data/layerConfig.json")
        )

        with open(column_sets_file, "w") as f:
            json.dump(column_sets, f)

        self.stdout.write(self.style.SUCCESS("Successfully created map detail pages"))
