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

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete", action="store_true", help="Delete existing map detail pages."
        )

    def create_layers(self, source):

        layers = []

        if source.type == "fill":
            fill_layer_list = ["draw", "border"]

            for layer in fill_layer_list:
                if layer == "draw":
                    name = f"{source.name} Interactive Layer"
                    id = f"{slugify(source.name)}-draw"
                    layers.append(
                        {
                            "name": name,
                            "id": id,
                            "type": "fill",
                            "layout": '{"visibility": "visible"}',
                            "paint": "{}",
                            "filter": "{}",
                            "is_interactive": True,
                        }
                    )

                elif layer == "border":
                    name = f"{source.name} Border"
                    id = f"{slugify(source.name)}-border"
                    layers.append(
                        {
                            "name": name,
                            "id": id,
                            "type": "line",
                            "layout": '{"visibility": "visible"}',
                            "paint": '{"line-color": "#777777","line-width": ["interpolate", ["linear"], ["zoom"], 0, 0, 7, 1],"line-opacity": 0.8}',
                            "filter": "{}",
                            "is_interactive": False,
                        }
                    )

                else:
                    continue

        if source.type == "circle":
            name = f"{source.name} Centroids"
            id = f"{slugify(source.name)}-centroids"
            layers.append(
                {
                    "name": name,
                    "id": id,
                    "type": "circle",
                    "layout": '{"visibility": "none"}',
                    "paint": "{}",
                    "filter": "{}",
                    "is_interactive": False,
                }
            )

        return layers

    def create_problem(self, problem, state, place_name, count, unit_type):

        parent_page = MapIndexPage.objects.get(title=state)

        if place_name:
            title = "{}, {} {}".format(place_name, state, problem["pluralNoun"])
        else:
            title = "{} {}".format(state, problem["pluralNoun"])

        # make a slug out of the state name and the problem plural noun
        slug = slugify("{}-{}-{}".format(state, problem["pluralNoun"], count))

        # create a new map detail page
        new_page = MapDetailPage(
            title=title,
            slug=slug,
            unit_count=problem["numberOfParts"],
            unit_name=problem["name"],
            unit_name_plural=problem["pluralNoun"],
            unit_type=unit_type,
        )

        # set the parent page
        parent_page.add_child(instance=new_page)

        # save the new page
        new_page.save_revision().publish()

        return new_page

    def handle(self, *args, **options):
        count = 12345

        # If the delete argument is passed, delete all existing map detail pages
        if options["delete"]:
            MapDetailPage.objects.all().delete()
            Source.objects.all().delete()

        location = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../data/districtr/assets/data/")
        )

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

                    new_pages = []

                    for problem in item["districtingProblems"]:
                        unit_type = item["units"][0]["unitType"]
                        page = self.create_problem(
                            problem, state, place_name, count, unit_type
                        )
                        count += 1
                        new_pages.append(page)

                    # if the map has tilesets, create a Source object for each one
                    sources = []
                    problem_bounds = None
                    for unit in item["units"]:
                        problem_bounds = unit["bounds"]

                        if place_name:
                            name = "{} - {} - {}".format(
                                state, place_name, unit["name"]
                            )
                        else:
                            name = "{} - {}".format(state, unit["name"])

                        if unit["tilesets"]:
                            for tileset in unit["tilesets"]:
                                source_layer = tileset["sourceLayer"]

                                # if the item has a name, use it. Create a location name = state + unit name

                                source_url = tileset["source"]["url"]

                                # get or create the source object
                                source, created = Source.objects.get_or_create(
                                    url=source_url,
                                    defaults={
                                        "name": name,
                                        "type": tileset["type"],
                                        "source_type": tileset["source"]["type"],
                                        "source_layer": source_layer,
                                    },
                                )

                                if created:
                                    # print a message to the console
                                    self.stdout.write(
                                        self.style.NOTICE(f"**  Source: {source.name}")
                                    )

                                sources.append(source)

                    # add the sources to the map detail pages and the bounds
                    for page in new_pages:
                        stream_data = []

                        for source in sources:
                            layers = self.create_layers(source)

                            stream_data.append(
                                {
                                    "type": "sources",
                                    "value": [
                                        {
                                            "source": source.id,
                                            "layers": layers,
                                        }
                                    ],
                                }
                            )

                        page.sources = StreamValue(
                            stream_block=page.sources.stream_block,
                            stream_data=stream_data,
                            is_lazy=True,
                        )

                        page.bounds_sw = Point(
                            (problem_bounds[0][0], problem_bounds[0][1]), srid=4326
                        )
                        page.bounds_ne = Point(
                            (problem_bounds[1][0], problem_bounds[1][1]), srid=4326
                        )

                        page.save_revision().publish()
