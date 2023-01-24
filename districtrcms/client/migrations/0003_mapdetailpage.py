# Generated by Django 4.0.8 on 2022-12-30 13:26

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0078_referenceindex'),
        ('client', '0002_mapindexpage_alter_homepage_options_homepage_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapDetailPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.RichTextField(blank=True)),
                ('unit_count', models.IntegerField(default=1)),
                ('unit_type', models.CharField(default='unit', max_length=255)),
                ('unit_name', models.CharField(default='unit', max_length=255)),
                ('unit_name_plural', models.CharField(default='units', max_length=255, verbose_name='Unit Name (Plural)')),
            ],
            options={
                'verbose_name': 'Map Detail Page',
            },
            bases=('wagtailcore.page',),
        ),
    ]
