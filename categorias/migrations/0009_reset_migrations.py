from django.db import migrations


def reset_migration_state(apps, schema_editor):
    """
    Reset migration state for categorias app
    """
    # This migration will be used to reset the migration state
    # It doesn't need to do anything specific
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0008_clean_migration'),
    ]

    operations = [
        migrations.RunPython(reset_migration_state, reverse_code=migrations.RunPython.noop),
    ] 