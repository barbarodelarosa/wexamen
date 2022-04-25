# Generated by Django 4.0.4 on 2022-04-25 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0003_planpago'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_type', models.CharField(choices=[('PRO', 'PRO'), ('MEDIO', 'MEDIO'), ('BASICO', 'BASICO')], max_length=25)),
                ('title', models.CharField(max_length=25)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Precio')),
            ],
        ),
        migrations.AddField(
            model_name='planpago',
            name='plan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='perfil.plan'),
            preserve_default=False,
        ),
    ]