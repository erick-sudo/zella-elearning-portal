from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect

from .models import ZellaUser, Unit, Question, Quiz, Course, Course, UnitRegistration, Choice, AssignmentSubmission

from django.core.exceptions import ValidationError

import json, pprint

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        courses = Course.objects.all()
        return render(request, 'zella/profile.html', {'user': request.user, 'courses': courses})
    else:
        return HttpResponseRedirect('/zella/login')

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/zella/')
        return render(request, "zella/login.html")
    elif request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        try:
            user = ZellaUser.objects.get(username=username)
            if user.is_active:
                # Correct password
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    # User is marked "active"
                    auth.login(request, user)
                    # Redirect to a success page.
                    #return render(request, "zella/index.html")
                    return HttpResponseRedirect('/zella/')
                else:
                    return render(request, "zella/login.html", {'error': 'Wrong Password!', 'username': username, 'password': password})
            else:
                return render(request, "zella/login.html", {'error': 'Pending Activation', 'username': username, 'password': password})
        except ZellaUser.DoesNotExist:
            # Show an error message
            return render(request, "zella/login.html", {'error': 'username does not exist', 'username': username, 'password': password})

def register(request):
    if request.method == 'GET':
        return render(request, "zella/register.html")
    else:
        username = request.POST.get('username', '')
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if(password != confirm_password):
            print("Passwords did not match")
            return render(request, 'zella/register.html', {
                'username': username,
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'password': password,
                'confirm_password': confirm_password
            })

        try:
            ZellaUser.objects.create_user(username=username, firstname=firstname, lastname=lastname, email=email, password=password)
        except ValidationError:
            print("Validation Errors")
            return render(request, 'zella/register.html', {
                'username': username,
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'password': password,
                'confirm_password': confirm_password
            })
        except:
            return render(request, 'zella/register.html', {
                'integrity': "Username already taken",
                'username': username,
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'password': password,
                'confirm_password': confirm_password
            })

        return HttpResponseRedirect('/zella/login')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/zella/login')

def getRegisteredUnits(pk):
    registered_units = UnitRegistration.objects.filter(student_id=pk)
    units = [ reg.unit for reg in registered_units]
    quiz_sets = ([ unit.quiz_set.all() for unit in units ])
    spread_quizes = []
    for quiz_set in quiz_sets:
        spread_quizes = [*spread_quizes, *quiz_set]
    return spread_quizes

def quizes(request):
    if request.user.is_authenticated:
        return render(request, 'zella/quizes.html', { 'quizes': getRegisteredUnits(request.user.pk) })
    else:
        return HttpResponseRedirect('/zella/login')
    

def startquiz(request, quiz_id):
    if request.user.is_authenticated:
        quizs = Quiz.objects.all()
        quiz = Quiz.objects.get(id=quiz_id)
        questions = Question.objects.filter(quiz_id=quiz_id)
        submitted = True
        try:
            AssignmentSubmission.objects.get(quiz_id=quiz.id, student_id=request.user.pk)
        except AssignmentSubmission.DoesNotExist:
            submitted = False
        return render(request, 'zella/quizes.html', { 'quizes': getRegisteredUnits(request.user.pk), 'questions': questions, 'quiz': quiz, 'submitted': submitted })
    else:
        return HttpResponseRedirect('/zella/login')


def profile(request):
    if request.user.is_authenticated:
        courses = Course.objects.all()
        return render(request, 'zella/profile.html', {'user': request.user, 'courses': courses})
    else:
        return HttpResponseRedirect('/zella/login')

def units(request):
    if request.user.is_authenticated:
        zella_user = ZellaUser.objects.get(username=request.user.username)
        units = zella_user.unitregistration_set.all()
        all_units = Unit.objects.all()
        return render(request, 'zella/units.html', {'registered_units': units, 'units': all_units, 'user': request.user})
    else:
        return HttpResponseRedirect('/zella/login')
    
def register_unit(request, student_id, unit_id):
    if request.user.is_authenticated:
        try:
            UnitRegistration.objects.get(unit_id=unit_id, student_id=student_id)
        except UnitRegistration.DoesNotExist:
            UnitRegistration.objects.create(unit_id=unit_id, student_id=student_id)
        finally:
            return HttpResponseRedirect('/zella/units')
    else:
        return HttpResponseRedirect('/zella/login')

def courses(request):
    if request.user.is_authenticated:
        courses = Course.objects.all()
        return render(request, 'zella/courses.html', { 'courses': courses})
    else:
        return HttpResponseRedirect('/zella/login')
    
def submit_assignment(request, student_id, quiz_id):
    answers = [[int(key[-1]), int(value[0])] for key, value in request.POST.lists() if key.startswith('question')]
    marking = [ Choice.objects.get(pk=answer[1]).correct for answer in answers]
    score = ((len([True for mark in marking if mark is True])/len(marking))*100)
    
    submission = AssignmentSubmission.objects.create(student_id=student_id, quiz_id=quiz_id, score=score)

    return HttpResponseRedirect('/zella/grades/'+str(student_id))

def grades(request, student_id):
    if request.user.is_authenticated:
        zella_user = ZellaUser.objects.get(username=request.user.username)
        grades = zella_user.assignmentsubmission_set.all()
        return render(request, 'zella/grades.html', { 'grades': grades})
    else:
        return HttpResponseRedirect('/zella/login')
