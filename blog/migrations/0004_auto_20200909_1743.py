# Generated by Django 3.1 on 2020-09-09 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_delete_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-id']},
        ),
    ]
