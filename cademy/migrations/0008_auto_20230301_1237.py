# Generated by Django 3.2.9 on 2023-03-01 04:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cademy', '0007_cademy'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MathCademy',
        ),
        migrations.DeleteModel(
            name='TechnologyCademy',
        ),
        migrations.AlterModelOptions(
            name='cademy',
            options={'verbose_name_plural': '学院'},
        ),
        migrations.AlterField(
            model_name='cademy',
            name='category',
            field=models.IntegerField(choices=[(1, '数学类'), (2, '工具类')], default=1, verbose_name='类别'),
        ),
    ]
