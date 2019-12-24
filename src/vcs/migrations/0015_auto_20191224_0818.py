# Generated by Django 3.0.1 on 2019-12-24 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcs', '0014_auto_20191224_0148'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='group',
            new_name='university_group',
        ),
        migrations.RemoveField(
            model_name='group',
            name='id',
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=6, primary_key=True, serialize=False),
        ),
    ]
