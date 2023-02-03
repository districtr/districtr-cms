import json
import os

from django.core.management.base import BaseCommand
from rest_framework.test import APIClient


class Command(BaseCommand):
    help = "Bakes API data into JSON files."

    def handle(self, *args, **options):

        dir_path = os.path.dirname(os.path.realpath(__file__))

        output_dir = os.path.join(dir_path, "../data/bakery")
        state_dir = os.path.join(output_dir, "state")
        county_dir = os.path.join(output_dir, "county")
        problem_dir = os.path.join(output_dir, "problem")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if not os.path.exists(state_dir):
            os.makedirs(state_dir)

        if not os.path.exists(county_dir):
            os.makedirs(county_dir)

        if not os.path.exists(problem_dir):
            os.makedirs(problem_dir)

        api_url = "http://testserver/wagtail-api/pages/"

        client = APIClient()

        client.credentials(
            HTTP_AUTHORIZATION="Token b93a97af195a8d210941fdaa8901639b14f2003a"
        )
        response = client.get(
            api_url,
            {
                "format": "json",
                "child_of": "4",
                "order": "title",
                "limit": "100",
                "fields": "*",
            },
            format="json",
        )
        response = json.loads(response.content)

        for state in response["items"]:
            print(state)
            state_id = state["id"]

            output_file = os.path.join(state_dir, state["meta"]["slug"] + ".json")

            county_response = client.get(
                api_url,
                {
                    "format": "json",
                    "child_of": state_id,
                    "type": "client.MapIndexPage",
                    "order": "title",
                    "limit": "1000",
                    "fields": "*",
                },
                format="json",
            )
            state["counties"] = json.loads(county_response.content)["items"]

            problem_response = client.get(
                api_url,
                {
                    "format": "json",
                    "child_of": state_id,
                    "type": "client.MapDetailPage",
                    "order": "title",
                    "limit": "1000",
                    "fields": "*",
                },
                format="json",
            )
            state["problems"] = json.loads(problem_response.content)["items"]

            with open(output_file, "w") as outfile:
                print(state)
                json.dump(state, outfile)
