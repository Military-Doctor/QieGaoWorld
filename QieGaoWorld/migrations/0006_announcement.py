# Generated by Django 2.0.7 on 2018-07-10 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QieGaoWorld', '0005_auto_20180710_0321'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_time', models.IntegerField(default=0)),
                ('username', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=512)),
                ('type', models.IntegerField(default=0)),
            ],
        ),
    ]