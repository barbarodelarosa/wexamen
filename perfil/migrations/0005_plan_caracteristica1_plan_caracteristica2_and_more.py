# Generated by Django 4.0.4 on 2022-04-25 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0004_plan_planpago_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='caracteristica1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='caracteristica2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='caracteristica3',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='caracteristica4',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='caracteristica5',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='plan_type',
            field=models.CharField(choices=[('BASICO', 'BASICO'), ('PRO', 'PRO'), ('MEDIO', 'MEDIO')], max_length=25),
        ),
        migrations.AlterField(
            model_name='planpago',
            name='plan_type',
            field=models.CharField(choices=[('BASICO', 'BASICO'), ('PRO', 'PRO'), ('MEDIO', 'MEDIO')], max_length=25),
        ),
    ]
