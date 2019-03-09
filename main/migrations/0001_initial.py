# Generated by Django 2.1.7 on 2019-03-09 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('comment', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('capacity', models.IntegerField()),
                ('projector', models.BooleanField(default=False)),
                ('tv', models.BooleanField(default=False)),
                ('air_conditioning', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='rooms',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Room'),
        ),
    ]
