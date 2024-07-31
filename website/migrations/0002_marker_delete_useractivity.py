# Generated by Django 5.0.6 on 2024-07-30 15:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.DeleteModel(
            name='UserActivity',
        ),
    ]