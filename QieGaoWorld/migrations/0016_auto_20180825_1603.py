# Generated by Django 2.0.7 on 2018-08-25 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QieGaoWorld', '0015_auto_20180725_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='uuid',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AlterField(
            model_name='user',
            name='permissions',
            field=models.CharField(default='%police_cases_watch%police_cases_add%declaration_animals%declaration_buildings%declaration_watch% ', max_length=2048),
        ),
    ]
