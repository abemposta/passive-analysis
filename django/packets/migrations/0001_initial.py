# Generated by Django 3.0.8 on 2020-08-27 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25)),
                ('password', models.CharField(max_length=50)),
                ('token', models.CharField(max_length=100)),
            ],
        ),
    ]
