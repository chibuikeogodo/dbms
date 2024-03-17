from django.contrib import admin
from .models import Staff,Schools,Student,Program,Country,Volunteer,VFYear,EmergencyContact,\
    Sponsor,VolunteerEmergencyContact,ProgramExpenses

admin.site.register(Program)
admin.site.register(Country)
admin.site.register(Schools)
admin.site.register(Staff)
admin.site.register(Volunteer)
admin.site.register(Student)
admin.site.register(VFYear)
admin.site.register(EmergencyContact)
admin.site.register(Sponsor)
admin.site.register(VolunteerEmergencyContact)
admin.site.register(ProgramExpenses)

