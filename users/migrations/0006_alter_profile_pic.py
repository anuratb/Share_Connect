# Generated by Django 3.2.4 on 2021-06-30 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(default='default.png', upload_to=''),
        ),
    ]
