# Generated by Django 4.2.3 on 2023-07-12 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userincome', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userincome',
            options={'ordering': ['-date'], 'verbose_name_plural': 'Income'},
        ),
    ]