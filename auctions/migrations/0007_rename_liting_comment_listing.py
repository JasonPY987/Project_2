# Generated by Django 4.1.3 on 2022-12-23 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='liting',
            new_name='listing',
        ),
    ]