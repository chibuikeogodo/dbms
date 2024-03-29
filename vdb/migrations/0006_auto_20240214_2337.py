# Generated by Django 3.2.23 on 2024-02-14 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vdb', '0005_alter_program_cohort'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=50)),
                ('image', models.ImageField(default=None, upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='program',
            name='name',
            field=models.CharField(choices=[('ASCG', 'ASCG'), ('CBC', 'CBC'), ('DSC', 'DSC'), ('SSC', 'SSC')], max_length=10),
        ),
    ]
