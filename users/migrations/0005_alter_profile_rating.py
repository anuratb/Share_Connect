# Generated by Django 3.2.4 on 2021-06-30 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210628_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
