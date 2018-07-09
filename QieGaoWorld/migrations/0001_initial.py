# Generated by Django 2.0.7 on 2018-07-08 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enable', models.BooleanField(default=True)),
                ('key', models.CharField(max_length=100)),
                ('time_start', models.IntegerField(default=0)),
                ('time_end', models.IntegerField(default=0)),
                ('time_aviliable', models.IntegerField(default=0)),
                ('usage_use', models.IntegerField(default=0)),
                ('usage_all', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('binding_user', models.CharField(max_length=100)),
                ('comment', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('username_md5', models.CharField(max_length=100)),
                ('password_md5', models.CharField(max_length=100)),
                ('userdata', models.CharField(max_length=65536)),
                ('email', models.CharField(max_length=100)),
                ('qq', models.CharField(max_length=100)),
                ('ban', models.CharField(max_length=100)),
            ],
        ),
    ]
