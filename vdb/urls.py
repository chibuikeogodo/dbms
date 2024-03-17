from django.contrib import admin
from django.urls import path, include
from .views import home, programs, staff, volunteer,delete_student,\
    delete_staff,login_view,logout,search_students,search_staff,student_details,\
    sponsors_page,staff_details,volunteer_details,update_student,add_program,delete_program,\
    add_emergency_contact,delete_emergency_contact,update_expenses,expenses,sponsors_page,\
    delete_volunter_emergency_contact


urlpatterns = [
    path('', home, name='home'),
    path('programs/', programs, name='programs'),
    path('login', login_view, name='login'),
    path('staff', staff, name='staff'),
    path('volunteers', volunteer, name='volunteers'),
    path('student/<int:student_id>/delete/', delete_student, name='delete_student'),
    path('remove/<int:staff_id>/', delete_staff, name='delete_staff'),
    path('logout/', logout, name='logout'),
    path('programs/search/', search_students, name='search_students'),
    path('staff/search/', search_staff, name='search_staffs'),
    path('students/<int:id>/', student_details, name='student_details'),
    path('update-student/<int:id>/', update_student, name='update_student'),
    path('staff/<int:id>/', staff_details, name='staff_details'),
    path('volunteers/<int:volunteer_id>/', volunteer_details, name='volunteer_details'),
    path('sponsors/', sponsors_page, name='sponsors_page'),
    path('student/<int:student_id>/add_program/', add_program, name='add_program'),
    path('student/<int:student_id>/delete_program/<int:program_id>/', delete_program, name='delete_program'),
    path('staff/<int:staff_id>/add_emergency_contact/', add_emergency_contact, name='add_emergency_contact'),
    path('staff/<int:staff_id>/emergency_contact/<int:contact_id>/delete/', delete_emergency_contact,
         name='delete_emergency_contact'),
    path('volunteer/<int:staff_id>/volunteer_emergency_contact/<int:contact_id>/delete/', delete_volunter_emergency_contact,
         name='delete_volunteer_emergency_contact'),
    path('expenses/', expenses, name='expenses'),
    path('update-expense/', update_expenses, name='update_expenses'),

]
