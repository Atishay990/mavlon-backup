# Generated by Django 4.1.3 on 2023-02-15 07:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_eventdata_delete_segmentdata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventdata",
            name="openAt",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]