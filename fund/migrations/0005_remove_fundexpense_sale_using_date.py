# Generated by Django 3.2.9 on 2022-02-07 02:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('fund', '0004_fundexpense_need_buy_again'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fundexpense',
            name='sale_using_date',
        ),
    ]