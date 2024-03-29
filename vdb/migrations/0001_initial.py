# Generated by Django 3.2.23 on 2024-02-14 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('num_of_students', models.PositiveBigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100)),
                ('chapter', models.CharField(max_length=100)),
                ('program_type', models.CharField(choices=[('ASCG', 'ASCG'), ('CBC', 'CBC'), ('DSC', 'DSC')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Schools',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_id', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('date_joined', models.DateField()),
                ('active', models.BooleanField(default=True)),
                ('position', models.CharField(max_length=100)),
                ('skill', models.CharField(default=None, max_length=100)),
                ('location', models.CharField(default=None, max_length=100)),
                ('address', models.CharField(default=None, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VFYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveBigIntegerField(default=2014)),
                ('target_number_of_students', models.PositiveBigIntegerField(default=0)),
                ('current_year', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('program', models.ManyToManyField(related_name='volunteers', to='vdb.Program')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('best_subjects', models.CharField(choices=[('English', 'English'), ('Mathematics', 'Mathematics'), ('Physics', 'Physics'), ('Chemistry', 'Chemistry'), ('Biology', 'Biology'), ('Economics', 'Economics'), ('Government', 'Government')], max_length=50)),
                ('worst_subject', models.CharField(choices=[('English', 'English'), ('Mathematics', 'Mathematics'), ('Physics', 'Physics'), ('Chemistry', 'Chemistry'), ('Biology', 'Biology'), ('Economics', 'Economics'), ('Government', 'Government')], max_length=50)),
                ('student_class', models.CharField(choices=[('SS1', 'SS1'), ('SS2 [Art]', 'SS2 [Art]'), ('SS2 [Science]', 'SS2 [Science]'), ('SS3 [Art]', 'SS3 [Art]'), ('SS3 [Science]', 'SS3 [Science]')], max_length=50)),
                ('date_of_birth', models.DateField(null=True)),
                ('program_year', models.PositiveIntegerField()),
                ('program_quarter', models.PositiveBigIntegerField(blank=True, default=1)),
                ('parents_name', models.CharField(max_length=50)),
                ('parent_email', models.CharField(blank=True, max_length=60, null=True)),
                ('house_address', models.CharField(max_length=60)),
                ('English', models.CharField(blank=True, default=None, max_length=1, null=True)),
                ('Mathematics', models.CharField(blank=True, default=None, max_length=1, null=True)),
                ('Physics', models.CharField(blank=True, default=None, max_length=1, null=True)),
                ('Chemistry', models.CharField(blank=True, default=None, max_length=1, null=True)),
                ('Biology', models.CharField(blank=True, default=None, max_length=1, null=True)),
                ('Civic', models.CharField(blank=True, default=None, max_length=1, null=True)),
                ('Economics', models.CharField(blank=True, default=None, max_length=1, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='vdb.country')),
                ('program', models.ManyToManyField(related_name='students_attended', to='vdb.Program')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='vdb.schools')),
            ],
        ),
        migrations.AddField(
            model_name='program',
            name='students',
            field=models.ManyToManyField(related_name='attended_programs', to='vdb.Student'),
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('relationship', models.CharField(default=None, max_length=50)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emergency_contacts', to='vdb.staff')),
            ],
        ),
    ]
