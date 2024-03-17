# Generated by Django 3.2.23 on 2024-02-14 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vdb', '0003_alter_student_program'),
    ]

    operations = [
        migrations.RenameField(
            model_name='program',
            old_name='chapter',
            new_name='duration',
        ),
        migrations.AddField(
            model_name='program',
            name='cohort',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], default=None, max_length=50),
        ),
    ]