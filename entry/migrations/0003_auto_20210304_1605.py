# Generated by Django 3.0.5 on 2021-03-04 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0002_auto_20210304_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=200, null=True, unique=True),
        ),
    ]