# Generated by Django 3.2.9 on 2021-12-31 09:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('fund', '0030_fund_best_transaction_rule_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundexpense',
            name='split_hold',
            field=models.IntegerField(default=0, verbose_name='拆分'),
        ),
        migrations.AlterField(
            model_name='fundexpense',
            name='deal_at',
            field=models.DateField(db_index=True, verbose_name='交易日期'),
        ),
    ]