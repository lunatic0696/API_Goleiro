# Generated by Django 2.1.7 on 2019-09-10 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('parteDoCorpo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Fisioterapeuta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='', max_length=100)),
                ('clinica', models.CharField(max_length=30)),
                ('descricao', models.CharField(max_length=30)),
                ('telefone', models.CharField(max_length=20)),
                ('crm', models.CharField(max_length=20)),
                ('dt_nascimento', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('telefone', models.CharField(max_length=20)),
                ('cpf', models.CharField(max_length=20)),
                ('dt_nascimento', models.DateField()),
                ('historico', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Sessao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_realizada', models.DateTimeField(auto_now_add=True)),
                ('exercicio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sessoes', to='kinect.Exercicio')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sessoes', to='kinect.Paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Tempo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tempo', models.TimeField()),
                ('sessao', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tempos', to='kinect.Sessao')),
            ],
        ),
        migrations.CreateModel(
            name='Tratamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condicao', models.TextField()),
                ('avaliacao', models.TextField()),
                ('fisioterapeuta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tratamentos', to='kinect.Fisioterapeuta')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tratamentos', to='kinect.Paciente')),
            ],
        ),
        migrations.AddField(
            model_name='sessao',
            name='tratamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sessoes', to='kinect.Tratamento'),
        ),
    ]
