from django.db import migrations


def generate_superuser(apps, schema_editor):
    """Create a new superuser """
    from django.contrib.auth import get_user_model
    from django.conf import settings

    superuser = get_user_model().objects.create_superuser(
        name="Super User",
        email="admin@kora.1kb.pl",
        password="admin",
    )
    superuser.save()


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(generate_superuser),
    ]
