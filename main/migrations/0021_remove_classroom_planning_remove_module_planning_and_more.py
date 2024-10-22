# Generated by Django 4.2.6 on 2024-06-24 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_planning_user_alter_teacher_modules'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='planning',
        ),
        migrations.RemoveField(
            model_name='module',
            name='planning',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='planning',
        ),
        migrations.AddField(
            model_name='classroom',
            name='planning',
            field=models.ManyToManyField(blank=True, null=True, related_name='classrooms', to='main.planning'),
        ),
        migrations.AddField(
            model_name='module',
            name='planning',
            field=models.ManyToManyField(blank=True, null=True, related_name='modules', to='main.planning'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='planning',
            field=models.ManyToManyField(blank=True, null=True, related_name='teachers', to='main.planning'),
        ),
    ]
