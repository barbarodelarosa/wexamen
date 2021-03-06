# Generated by Django 4.0.4 on 2022-04-25 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0007_profile_affiliated_profile_affiliated_url_profile_ci_and_more'),
    ]

    operations = [
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
        migrations.CreateModel(
            name='AffiliateApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('aprovated', models.BooleanField(default=False)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perfil.profile')),
            ],
        ),
    ]
