# Generated by Django 2.1.12 on 2019-10-05 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('daphne_context', '0002_auto_20190923_2316'),
    ]

    operations = [
        migrations.CreateModel(
            name='DialogueContext',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_clarifying_input', models.BooleanField()),
                ('dialogue_history', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='daphne_context.DialogueHistory')),
            ],
        ),
    ]
