from django import forms
from . models import Staff,Student,Schools,Program,Volunteer,EmergencyContact,Sponsor,VolunteerEmergencyContact


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('id','first_name', 'last_name', 'school','student_class', 'date_of_birth','best_subjects',
                  'worst_subject','parents_name','parent_email','house_address','program_year', 'email', 'phone_number',
                  'country','English','Mathematics','Physics','Chemistry','Biology','Civic','Economics')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter Last Name'}),
            'school': forms.Select(attrs={'placeholder': 'Enter First Name'}),
            'date_of_birth': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            'program_year': forms.NumberInput(attrs={'placeholder': 'Enter Program Year'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
            'country': forms.Select(attrs={'placeholder': 'Enter Country'}),
            'best_subjects': forms.Select(attrs={'placeholder': 'Select Subject'}),
            'worst_subject': forms.Select(attrs={'placeholder': 'Select Subject'}),
            'student_class': forms.Select(attrs={'placeholder': 'Select Class'}),
            'parents_name': forms.TextInput(attrs={'placeholder': 'Enter Parent Name'}),
            'parent_email': forms.TextInput(attrs={'placeholder': 'Enter Parent Email'}),
            'house_address': forms.TextInput(attrs={'placeholder': 'Enter House Address'}),

        }


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'cohort', 'topic', 'duration']

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'address', 'phone_number', 'email','relationship']

class VolunteerEmergencyContactForm(forms.ModelForm):
    class Meta:
        model = VolunteerEmergencyContact
        fields = ['name', 'address', 'phone_number', 'email','relationship']

class StaffForm(forms.Form):
    class Meta:
        model = Staff
        fields = ['start_id','first_name','last_name','email','phone_number','date_joined','active','position','skill',
                  'location','address']

class VolunteerForm(forms.Form):
    class Meta:
        model = Volunteer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'start_date', 'end_date',
                  'program']


class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = ['name', 'logo']