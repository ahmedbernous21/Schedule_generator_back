# Generated by Django 4.2.6 on 2024-06-18 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_module_planning'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='planning',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classrooms', to='main.planning'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='planning',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teachers', to='main.planning'),
        ),
    ]