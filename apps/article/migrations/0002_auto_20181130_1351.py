# Generated by Django 2.0 on 2018-11-30 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='pub_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
