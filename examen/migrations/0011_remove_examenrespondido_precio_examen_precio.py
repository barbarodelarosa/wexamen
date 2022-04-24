# Generated by Django 4.0.4 on 2022-04-24 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examen', '0010_examenrespondido_precio_profile_presupuesto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examenrespondido',
            name='precio',
        ),
        migrations.AddField(
            model_name='examen',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Precio del examen'),
        ),
    ]
