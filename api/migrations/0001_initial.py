# Generated by Django 3.2 on 2021-04-29 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('idd', models.CharField(max_length=50, unique=True)),
                ('age', models.IntegerField()),
                ('self_url', models.CharField(max_length=100)),
                ('albums_url', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('duration', models.FloatField()),
                ('times_played', models.IntegerField()),
                ('idd', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('gen', models.CharField(max_length=50)),
                ('idd', models.CharField(max_length=50, unique=True)),
                ('artist_url', models.CharField(max_length=100)),
                ('self_url', models.CharField(max_length=100)),
                ('artist_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.artist', to_field='idd')),
            ],
        ),
    ]
