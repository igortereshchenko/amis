# Generated by Django 3.0.1 on 2019-12-24 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcs', '0002_auto_20191223_2355'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='test@mail.com', max_length=254, unique=True),
            preserve_default=False,
        ),
    ]
