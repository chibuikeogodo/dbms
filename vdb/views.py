from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import CreateView
from django.utils import timezone

from .models import Program,Schools,Staff,Student, Volunteer, Country,VFYear,EmergencyContact, Sponsor, ProgramExpenses, VolunteerEmergencyContact
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from .serializer import CountrySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import StudentForm, ProgramForm, EmergencyContactForm, SponsorForm, VolunteerEmergencyContactForm


def get_program_page_context(request):
    # Page data
    programs = Program.objects.all()
    schools = Schools.objects.all()
    countries = Country.objects.all()

    # Pagination
    program_filter = request.GET.get('program')
    if program_filter:
        students = Student.objects.filter(program__name=program_filter).order_by('-id')
    else:
        students = Student.objects.all().order_by('-id')
    page = request.GET.get('page')
    paginator = Paginator(students, 5)
    students = paginator.get_page(page)

    context = {
        'students': students,
        'programs': programs,
        'program':program_filter,
        'schools': schools,
        'countries': countries,
        'program_filter': program_filter,
        'page': 'programs',
    }

    return context


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'pages/login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'pages/login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):

    # collect filter year and quarter value from user
    year = request.GET.get('year')
    quarter = request.GET.get('quarter')
    show_all_btn = False


    students_count = Student.objects.all()
    staffs_count = Staff.objects.count()
    volunteers_count = Volunteer.objects.count()
    cbc_count = Student.objects.filter(program__name='CBC')
    ssc_count = Student.objects.filter(program__name='SSC')
    dsc_count = Student.objects.filter(program__name='DSC')
    ascg_count = Student.objects.filter(program__name='ASCG')

    vf_year_target_percent_completed = None
    year_val = ""

    if year != None and year != "":

        print("year is ",year)
        students_count = students_count.filter(program_year=int(year))
        cbc_count = cbc_count.filter(program_year=int(year))
        ssc_count = ssc_count.filter(program_year=int(year))
        dsc_count = dsc_count.filter(program_year=int(year))
        ascg_count = ascg_count.filter(program_year=int(year))

        year_val += year

        if year != "2014":
            show_all_btn = True

        try:
            vf_year_target = VFYear.objects.get(year=year).target_number_of_students
            vf_year_target_percent_completed = int(100*students_count.count()/vf_year_target)

        except VFYear.DoesNotExist:
            pass

    if quarter != None:
        students_count = students_count.filter(program_quarter=int(quarter))
        cbc_count = cbc_count.filter(program_quarter=int(quarter))
        ssc_count = ssc_count.filter(program_quarter=int(quarter))
        dsc_count = dsc_count.filter(program_quarter=int(quarter))
        ascg_count = ascg_count.filter(program_quarter=int(quarter))

        year_val += f":Q{quarter}"

    # we will come back to country
    country_data = []
    country_max_count = 10

    countries = Country.objects.all()
    for country in countries:
        number_of_students_from_country = students_count.filter(country=country).count()
        if  number_of_students_from_country == 0:
            countries = countries.exclude(name=country.name)
        else:
            country_data.append(
                {
                    'name':country.name.upper()[:3],
                    'count':number_of_students_from_country,
                    'percentage': int(100 * number_of_students_from_country / country_max_count)
                }
            )

    countries_count = len(countries)

    context ={
        'students_count': students_count.count(),
        'staffs_count':staffs_count,
        'volunteers_count':volunteers_count,
        'cbc_count':cbc_count.count(),
        'ssc_count':ssc_count.count(),
        'dsc_count':dsc_count.count(),
        'ascg_count':ascg_count.count(),
        'countries_count':countries_count,
        'country_data':country_data,
        'country_max_count':country_max_count,
        'year':year,
        'year_val' : year_val,
        'show_all_btn':show_all_btn,
        'vf_year_target_percent_completed':vf_year_target_percent_completed,
        'page':'dashboard'

    }
    return render(request, 'sections/dashboard.html', context)


# This page below talks about anything that has to do with students and program
@login_required(login_url='login')
def programs(request):
    programs = Program.objects.all()
    schools = Schools.objects.all()
    countries = Country.objects.all()

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('programs')
        else:
            print(form.errors)
    else:
        form = StudentForm()

    # Pagination
    program_filter = request.GET.get('program')
    if program_filter:
        students = Student.objects.filter(program__name=program_filter).order_by('-id')
    else:
        students = Student.objects.all().order_by('-id')
    page = request.GET.get('page')
    paginator = Paginator(students, 5)
    students = paginator.get_page(page)

    context = {
        'students': students,
        'programs': programs,
        'schools': schools,
        'countries': countries,
        'program_filter': program_filter,
        'page': 'programs',
        'form': form,

    }
    return render(request, 'sections/programs.html', context)

@login_required(login_url='login')
def update_student(request,id):

    context = get_program_page_context(request)
    
    if request.method == "POST":
        try:
            student = Student.objects.get(id=id)
            form = StudentForm(request.POST,instance=student)

            if form.is_valid():
                form.save()
                return redirect('programs')
            else:
                context['form'] = form
                context['program_id'] = id
                context['form_page'] = "student"
                context['action'] = f"/update-student/{id}/"

        except Student.DoesNotExist:
            return redirect('programs')
        
        return render(request, 'sections/programs.html', context)
    return redirect('programs')

@login_required(login_url='login')
def search_students (request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        students = Student.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    else:
        students = Student.objects.all()

    return render(request, 'sections/programs.html',{
        'students':students,
        })


def student_details(request, id):
    student = get_object_or_404(Student, pk=id)
    programs = Program.objects.all().order_by('-id')

    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            program = form.save()
            student.program.add(program)
            return redirect('student_details', id=id)
    else:
        form = ProgramForm()

    context = {
        'student': student,
        'page': 'programs',
        'show_emergency_contacts': False,
        'show_grades': True,
        'show_programs': True,
        'form': form,
        'programs': programs,
    }

    return render(request, 'sections/student_details.html', context)

@login_required(login_url='login')
def delete_student(request, student_id):
    if request.method == 'POST':
        student = Student.objects.get(pk=student_id)
        student.delete()
        return redirect('programs')  # Redirect to the programs page after deletion
    else:
        return redirect('programs')

@login_required(login_url='login')
def add_program(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        program_id = request.POST.get('program')
        program = get_object_or_404(Program, pk=program_id)
        student.program.add(program)
        return redirect('student_details', id=student_id)
    return redirect('student_details', id=student_id)

@login_required(login_url='login')
def delete_program(request, student_id, program_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, pk=student_id)
        program = get_object_or_404(Program, pk=program_id)
        student.program.remove(program)
        return HttpResponseRedirect(reverse('student_details', args=[student_id]))
    return HttpResponseRedirect(reverse('student_details', args=[student_id]))

# Everything about Students and Progamme Ends here

@login_required(login_url='login')
def volunteer_details(request, volunteer_id):
    volunteer = get_object_or_404(Volunteer, pk=volunteer_id)
    if request.method == 'POST':
        emegency_form = VolunteerEmergencyContactForm(request.POST)
        if emegency_form.is_valid():
            emergency_contact = emegency_form.save(commit=False)
            emergency_contact.staff = volunteer
            emergency_contact.save()
            return redirect('volunteer_details',volunteer_id=volunteer_id)
    else:
         emegency_form=VolunteerEmergencyContactForm()

    volunter_emegency_contacts =VolunteerEmergencyContact.objects.filter(staff=volunteer)

    context = {
        'volunteer': volunteer,
        'emegency_form':emegency_form,
        'volunter_emegency_contacts':volunter_emegency_contacts,
        'show_emergency_contacts': True,

    }
    return render(request, 'sections/volunteer_details.html', context)

#This codes below are for anything concerning staff
@login_required(login_url='login')
def staff_details(request,id):
    staff = get_object_or_404(Staff, pk=id)
    if request.method == 'POST':
        emergency_form = EmergencyContactForm(request.POST)
        if emergency_form.is_valid():
            emergency_contact = emergency_form.save(commit=False)
            emergency_contact.staff = staff
            emergency_contact.save()
            return redirect('staff_details', id=id)
    else:
        emergency_form = EmergencyContactForm()

    emergency_contacts = EmergencyContact.objects.filter(staff=staff)

    context = {
        'page': 'staffs',
        'show_emergency_contacts': True,
        'show_grades': False,
        'show_programs': False,
        'staff': staff,
        'emergency_contacts': emergency_contacts,
        'emergency_form': emergency_form,
    }

    return render(request, 'sections/staff_details.html', context)


@login_required(login_url='login')
def search_staff (request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        staffs = Staff.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    else:
        staffs = Staff.objects.all()

    return render(request, 'sections/staff.html',{'staffs':staffs})

@login_required(login_url='login')
def staff(request):
    active = request.GET.get('status')
    staffs = Staff.objects.all().order_by('-id')

    if active == "YES":
        staffs = staffs.filter(active=True)

    paginator = Paginator(staffs, 5)
    page = request.GET.get('page')
    staffs = paginator.get_page(page)

    if request.method == 'POST':
        start_id = request.POST['start_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        date_joined = request.POST['date_joined']
        active = int(request.POST['active'])
        position = request.POST['position']
        skill = request.POST['skill']
        location = request.POST['location']
        address = request.POST['address']

        staff = Staff.objects.create(
            start_id=start_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            date_joined=date_joined,
            active=active == 1,
            position=position,
            skill=skill,
            location=location,
            address=address
        )
        staff.save()

        return redirect('staff')

    context = {
        'staffs': staffs,
        'page':'staffs'
    }
    return render(request, 'sections/staff.html', context)


@login_required(login_url='login')
def delete_staff(request, staff_id):
    if request.method == 'POST':
        staff = Staff.objects.get(pk=staff_id)
        staff.delete()
        return redirect(reverse('staff'))
    else:
        return redirect(reverse('staff'))

@login_required(login_url='login')
def add_emergency_contact(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            emergency_contact = form.save(commit=False)
            emergency_contact.staff = staff
            emergency_contact.save()
            return redirect('staff_detail', staff_id=staff_id)
    else:
        form = EmergencyContactForm()
    return render(request,'sections/staff_details.html', {'form': form, 'staff': staff})

@login_required(login_url='login')
def delete_emergency_contact(request, staff_id, contact_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    contact = get_object_or_404(EmergencyContact, pk=contact_id)
    if request.method == 'POST':
        contact.delete()
        return redirect('staff_details', id=staff_id)
    return render(request, 'pages/base.html', {'staff': staff, 'contact': contact})

@login_required(login_url='login')
def delete_volunter_emergency_contact(request, staff_id, contact_id):
    staff = get_object_or_404(Volunteer, pk=staff_id)
    contact = get_object_or_404(VolunteerEmergencyContact, pk=contact_id)
    if request.method == 'POST':
        contact.delete()
        return redirect('volunteer_details', volunteer_id=staff_id)  # Update id to volunteer_id
    return render(request, 'pages/base.html', {'staff': staff, 'contact': contact})

## This is the end of code for Staff


## This is the code for Volunteers
@login_required(login_url='login')
def volunteer(request):
    volunteers = Volunteer.objects.all()
    programs = Program.objects.all()
    paginator = Paginator(volunteers, 5)
    page = request.GET.get('page')
    volunteers = paginator.get_page(page)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        location = request.POST['location']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        program_ids = request.POST.getlist('program')


        volunteers_form = Volunteer.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            start_date=start_date,
            end_date=end_date,
            location=location,
        )
        volunteers_form.program.set(program_ids)
        volunteers_form.save()

        return redirect('volunteers')

    context = {
        'volunteers': volunteers,
        'page':'volunteers',
        'volunteers_form':'volunteers_form',
        'programs':programs,
    }
    return render(request, 'sections/volunteers.html', context)









@login_required(login_url='login')
def sponsors_page(request):
    if request.method == "POST":
        form = SponsorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('sponsors_page')
        else:
            print(form.errors)
    context = {
        'sponsor_form':SponsorForm(),
        'page':'sponsors',
        'sponsors':Sponsor.objects.all().order_by("-pk")
    }

    return render(request,
        'sections/sponsors.html',
        context
    )


@login_required(login_url='login')
def expenses(request):
    current_year = str(timezone.now().year)

    year = request.GET.get('year')

    if year is not None and len(year) == 4 and year < current_year:
        current_year = year

    try:
        expenses = ProgramExpenses.objects.get(year=current_year)
    except ProgramExpenses.DoesNotExist:
        expenses = None

    context = {
        'page': 'expenses',
        'data': expenses,
        'year': current_year
    }

    return render(request, 'sections/expenses.html', context)


@api_view(['POST'])
def update_expenses(request):
    data = request.POST
    year = data['year']
    col = data['column']
    row = data['row']

    try:
        expenses = ProgramExpenses.objects.get(year=year)
        expenses.columns = col
        expenses.row = row
        expenses.save()

    except ProgramExpenses.DoesNotExist:
        pass

    return Response({'msg': 'done'})





