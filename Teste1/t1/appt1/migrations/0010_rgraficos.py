# Generated by Django 4.2.6 on 2024-01-08 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appt1', '0009_novos_valores_delete_cria_gauge_delete_cria_grafico'),
    ]

    operations = [
        migrations.CreateModel(
            name='RGraficos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datae', models.TextField(max_length=255)),
            ],
        ),
    ]
