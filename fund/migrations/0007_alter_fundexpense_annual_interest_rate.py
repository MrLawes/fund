# Generated by Django 3.2.9 on 2025-02-07 03:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('fund', '0006_alter_fundexpense_annual_interest_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundexpense',
            name='annual_interest_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='投资回报年化率'),
        ),
    ]
