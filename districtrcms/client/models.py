from django.contrib.gis.db import models
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations
from django.http import HttpResponseRedirect
from rest_framework import serializers
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.models import register_snippet


class Migration(migrations.Migration):
    operations = [CreateExtension("postgis")]


@register_snippet
class Source(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(
        choices=[("fill", "Fill"), ("circle", "Circle")], max_length=255
    )
    source_layer = models.CharField(max_length=255, null=True, blank=True)
    source_type = models.CharField(
        choices=[("geojson", "GeoJSON"), ("vector", "Vector")], max_length=255
    )
    url = models.URLField()

    panels = [
        FieldPanel("name"),
        FieldPanel("url"),
        FieldPanel("type"),
        FieldPanel("source_layer"),
        FieldPanel("source_type"),
    ]

    search_fields = [
        index.SearchField("name", partial_match=True),
        index.SearchField("url", partial_match=True),
    ]

    api_fields = [
        APIField("name"),
        APIField("type"),
        APIField("source_layer"),
        APIField("source_type"),
        APIField("url"),
    ]

    def __str__(self):
        return self.name


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = "__all__"


class APISourceChooserBlock(SnippetChooserBlock):
    # Override the default representation of the block in the API so that all the fields can be served over the api
    def get_api_representation(self, value, context=None):
        return SourceSerializer(context=context).to_representation(value)


class HomePage(Page):
    class Meta:
        verbose_name = "Home Page"

    page_description = "This is the home page. Only one home page can exist."
    max_count = 1

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    api_fields = [
        APIField("title"),
        APIField("body"),
        APIField("live"),
        APIField("locale"),
    ]

    def serve(self, request):

        return HttpResponseRedirect(f"/wagtail-api/pages/{self.id}/")


class MapIndexPage(Page):
    class Meta:
        verbose_name = "Map Index Page"

    page_description = "This is the map index page. It indexs problems relate to itself and other child indexes."

    body = RichTextField(blank=True)

    parent_page_types = ["client.HomePage", "client.MapIndexPage"]
    subpage_types = ["client.MapIndexPage"]

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    api_fields = [
        APIField("title"),
        APIField("body"),
        APIField("live"),
        APIField("locale"),
    ]

    def serve(self, request):

        return HttpResponseRedirect(f"/wagtail-api/pages/{self.id}/")


class MapDetailPage(Page):
    class Meta:
        verbose_name = "Map Detail Page"

    page_description = "Configure a map and organize published results."

    body = RichTextField(blank=True)

    # Map Configuration Fields
    unit_count = models.IntegerField(default=1)
    unit_type = models.CharField(max_length=255, default="unit")
    unit_name = models.CharField(max_length=255, default="unit")
    unit_name_plural = models.CharField(
        max_length=255, default="units", verbose_name="Unit Name (Plural)"
    )
    bounds_sw = models.PointField(null=True, blank=True)
    bounds_ne = models.PointField(null=True, blank=True)

    # Map Sources and Layer Fields
    sources = StreamField(
        [
            (
                "sources",
                blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            ("source", APISourceChooserBlock(Source)),
                            (
                                "layers",
                                blocks.ListBlock(
                                    blocks.StructBlock(
                                        [
                                            ("name", blocks.CharBlock()),
                                            ("id", blocks.CharBlock()),
                                            (
                                                "type",
                                                blocks.ChoiceBlock(
                                                    choices=[
                                                        ("fill", "Fill"),
                                                        ("line", "Line"),
                                                        ("symbol", "Symbol"),
                                                        ("circle", "Circle"),
                                                    ]
                                                ),
                                            ),
                                            ("layout", blocks.RawHTMLBlock()),
                                            ("paint", blocks.RawHTMLBlock()),
                                            ("filter", blocks.RawHTMLBlock()),
                                            (
                                                "is_interactive",
                                                blocks.BooleanBlock(blank=True),
                                            ),
                                        ]
                                    )
                                ),
                            ),
                        ]
                    )
                ),
            )
        ],
        use_json_field=True,
        blank=True,
    )

    parent_page_types = ["client.MapIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel("unit_count"),
                FieldPanel("unit_type"),
                FieldPanel("unit_name"),
                FieldPanel("unit_name_plural"),
            ],
            heading="Map Configuration",
        ),
        FieldPanel("sources"),
    ]

    api_fields = [
        APIField("title"),
        APIField("body"),
        APIField("live"),
        APIField("locale"),
        APIField("sources"),
        APIField("unit_count"),
        APIField("unit_type"),
        APIField("unit_name"),
        APIField("unit_name_plural"),
        APIField("bounds_sw"),
        APIField("bounds_ne"),
    ]

    def serve(self, request):

        return HttpResponseRedirect(f"/wagtail-api/pages/{self.id}/")
