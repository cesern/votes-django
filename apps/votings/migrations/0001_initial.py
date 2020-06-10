# Generated by Django 2.0.2 on 2018-03-08 01:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0004_auto_20180306_2117'),
    ]

    operations = [
        migrations.CreateModel(
            name='IVoted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('votacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.Voting')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.Answer')),
                ('votacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.Voting')),
            ],
        ),
    ]