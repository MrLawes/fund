# Generated by Django 3.2.9 on 2023-02-07 02:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('cademy', '0005_toolscademy'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ToolsCademy',
            new_name='TechnologyCademy',
        ),
        migrations.AlterModelOptions(
            name='mathcademy',
            options={'verbose_name_plural': '数学类'},
        ),
        migrations.AlterModelOptions(
            name='technologycademy',
            options={'verbose_name_plural': '技术类'},
        ),
    ]