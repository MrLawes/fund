# Generated by Django 3.2.9 on 2023-07-27 04:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cademy', '0011_auto_20230414_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cademy',
            name='category',
            field=models.IntegerField(choices=[(1, '数学类'), (2, '工具类'), (3, '网络安全'), (4, '前端'), (5, '快速构建网站'), (6, 'Python')], default=1, verbose_name='类别'),
        ),
    ]
