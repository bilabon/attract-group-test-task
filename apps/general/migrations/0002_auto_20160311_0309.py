# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.core.management import call_command


def import_fixtures(apps, schema_editor):
    call_command('loaddata', '_initial_general.json')
    call_command('loaddata', '_initial_user.json')


class Migration(migrations.Migration):
    """
    Load initial fixtures for auth and general apps
    """

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_fixtures),
    ]
