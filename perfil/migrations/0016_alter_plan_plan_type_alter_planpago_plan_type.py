# Generated by Django 4.0.4 on 2022-04-26 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0015_alter_plan_plan_type_alter_planpago_plan_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='plan_type',
            field=models.CharField(choices=[('MEDIO', 'MEDIO'), ('BASICO', 'BASICO'), ('PRO', 'PRO')], max_length=25),
        ),
        migrations.AlterField(
            model_name='planpago',
            name='plan_type',
            field=models.CharField(choices=[('MEDIO', 'MEDIO'), ('BASICO', 'BASICO'), ('PRO', 'PRO')], max_length=25),
        ),
    ]