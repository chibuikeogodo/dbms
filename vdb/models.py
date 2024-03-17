from django.db import models
from django.utils import timezone
from .utils import get_current_quarter



class VFYear(models.Model):
    year = models.PositiveBigIntegerField(default=2014)
    target_number_of_students = models.PositiveBigIntegerField(default=0)
    current_year = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.year}"



class Country(models.Model):
    name = models.CharField(max_length=50)
    num_of_students = models.PositiveBigIntegerField(default=0)
    
    def __str__(self):
        return self.name


class Schools(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Program(models.Model):
    PROGRAM_CHOICES = [
        ('ASCG', 'ASCG'),
        ('CBC', 'CBC'),
        ('DSC', 'DSC'),
        ('SSC','SSC')
    ]
    cohort_choice = [
        ('1','1'),
        ('2','2'),
        ('3','3')
    ]

    topic = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    cohort = models.CharField(max_length=50, choices=cohort_choice,blank=True,null=True, default=0)
    name = models.CharField(max_length=10, choices=PROGRAM_CHOICES)
    students = models.ManyToManyField('Student', related_name='attended_programs')

    def __str__(self):
        return f"{self.students}"


class Student(models.Model):
    Class = (
        ('SS1', 'SS1'),
        ('SS2 [Art]', 'SS2 [Art]'),
        ('SS2 [Science]', 'SS2 [Science]'),
        ('SS3 [Art]', 'SS3 [Art]'),
        ('SS3 [Science]', 'SS3 [Science]')
    )
    Subjects = (
        ('English','English'),
        ('Mathematics', 'Mathematics'),
        ('Physics','Physics'),
        ('Chemistry','Chemistry'),
        ('Biology','Biology'),
        ('Economics','Economics'),
        ('Government','Government'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    school = models.ForeignKey(Schools, on_delete=models.CASCADE, related_name='students')
    best_subjects = models.CharField(max_length=50, choices=Subjects)
    worst_subject = models.CharField(max_length=50,choices=Subjects)
    student_class = models.CharField(max_length=50, choices=Class)
    date_of_birth = models.DateField(null=True)
    program_year = models.PositiveIntegerField()
    program_quarter = models.PositiveBigIntegerField(default=1,blank=True)
    program = models.ManyToManyField(Program, related_name='students_attended', blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='students')
    parents_name = models.CharField(max_length=50)
    parent_email = models.CharField(max_length=60, blank=True, null=True)
    house_address = models.CharField(max_length=60)
    English = models.CharField(max_length=1, blank=True, null=True, default=None)
    Mathematics = models.CharField(max_length=1, blank=True, null=True, default=None)
    Physics = models.CharField(max_length=1, blank=True, null=True, default=None)
    Chemistry = models.CharField(max_length=1, blank=True, null=True, default=None)
    Biology = models.CharField(max_length=1, blank=True, null=True, default=None)
    Civic = models.CharField(max_length=1, blank=True, null=True, default=None)
    Economics = models.CharField(max_length=1, blank=True, null=True, default=None)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)
    
    def update_program_quarter(self):
        self.program_quarter = get_current_quarter()
            
        self.save()



class Staff(models.Model):
    start_id = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    date_joined = models.DateField()
    active = models.BooleanField(default=True)
    position = models.CharField(max_length=100)
    skill = models.CharField(max_length=100, default=None)
    location = models.CharField(max_length=100, default=None)
    address = models.CharField(max_length=100, default=None)
    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class EmergencyContact(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    relationship = models.CharField(max_length=50, default=None)
    def __str__(self):
        return self.name


class Volunteer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    program = models.ManyToManyField(Program, related_name='volunteers')
    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

class VolunteerEmergencyContact(models.Model):
    staff = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='Volunteer_emergency_contacts')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    relationship = models.CharField(max_length=50, default=None)
    def __str__(self):
        return self.name


class ProgramExpenses(models.Model):
    year = models.CharField(unique=True, max_length=4)
    tag = models.CharField(max_length=50, blank=True)
    columns = models.TextField()  # comma seperated strings
    row = models.TextField()  # row1:col1/col2/col3;row2:col1/col2/col3

    def __str__(self):
        return self.year

    def save_expenses(self, data):
        columns = data['columns']
        row = data['rows']
        row_raw_data = ""

        for i in row:
            row_data = ""
            for field in i['fields']:
                if row_data != "":
                    row_data += f"/{field}"
                else:
                    row_data += field

            if row_raw_data != "":
                row_raw_data += f";{i['name']}:{row_data}"
            else:
                row_raw_data += f"{i['name']}:{row_data}"

        columns = ",".join(columns)
        self.columns = columns
        self.row = row_raw_data

        self.save()

    def decode_expense_data(self):
        columns = self.columns.split(",")
        rows = []
        raw_row_data = self.row.split(";")
        for row in raw_row_data:
            name, fields = row.split(":")
            rows.append({
                'name': name,
                'fields': fields.split('/')
            })

        return {
            'columns': columns,
            'rows': rows
        }


class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    logo = models.FileField()

    def __str__(self):
        return self.name