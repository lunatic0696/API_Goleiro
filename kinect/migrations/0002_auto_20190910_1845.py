# Generated by Django 2.1.7 on 2019-09-10 21:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kinect', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fisioterapeuta',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='fisioterapeuta', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paciente',
            name='genero',
            field=models.CharField(default='M', max_length=1),
        ),
        migrations.AddField(
            model_name='paciente',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='paciente', to=settings.AUTH_USER_MODEL),
        ),
    ]