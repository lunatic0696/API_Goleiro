# Generated by Django 2.2.5 on 2019-10-17 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kinect', '0004_remove_sessao_paciente'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempo',
            name='parteDoCorpo',
            field=models.TextField(default='Não informado'),
        ),
        migrations.AddField(
            model_name='tempo',
            name='toucher',
            field=models.TextField(default='Não informado'),
        ),
        migrations.AlterField(
            model_name='tempo',
            name='tempo',
            field=models.FloatField(default=0),
        ),
    ]
