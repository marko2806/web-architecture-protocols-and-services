# Generated by Django 3.2.16 on 2022-12-07 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BoardGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('min_players', models.IntegerField()),
                ('max_players', models.IntegerField()),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board_game_module.publisher')),
            ],
        ),
    ]
