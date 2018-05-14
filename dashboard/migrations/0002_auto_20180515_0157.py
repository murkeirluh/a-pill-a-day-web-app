# Generated by Django 2.0.5 on 2018-05-14 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intakes',
            name='time_taken',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='prescriptions',
            name='notes',
            field=models.TextField(default='None'),
        ),
    ]
