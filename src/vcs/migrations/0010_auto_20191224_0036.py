# Generated by Django 3.0.1 on 2019-12-24 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcs', '0009_auto_20191224_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='teacher_lectures',
            field=models.ManyToManyField(blank=True, to='vcs.Lecture'),
        ),
    ]
