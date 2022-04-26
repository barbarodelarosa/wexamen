# Generated by Django 4.0.4 on 2022-04-25 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0008_alter_plan_plan_type_alter_planpago_plan_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='plan_type',
            field=models.CharField(choices=[('PRO', 'PRO'), ('MEDIO', 'MEDIO'), ('BASICO', 'BASICO')], max_length=25),
        ),
        migrations.AlterField(
            model_name='planpago',
            name='plan_type',
            field=models.CharField(choices=[('PRO', 'PRO'), ('MEDIO', 'MEDIO'), ('BASICO', 'BASICO')], max_length=25),
        ),
    ]