# Generated by Django 2.0.2 on 2018-03-06 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tema', models.CharField(max_length=255)),
                ('pregunta', models.CharField(max_length=255)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='votacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.Voting'),
        ),
    ]
