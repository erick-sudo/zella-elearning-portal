from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from django.utils import timezone

from .managers import ZellaUserManager

# Create your models here.
class College(models.Model):
    name = models.CharField(max_length=100)
    abbr = models.CharField(max_length=15)

    def __str__(self):
        return self.name+" ("+self.abbr+")"

class Course(models.Model):
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    abbr = models.CharField(max_length=15)
    duration = models.IntegerField(default=4)

    def __str__(self):
        return self.name+" ("+self.abbr+")"
    
class Unit(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    abbr = models.CharField(max_length=15)

    def __str__(self):
        return self.course.abbr+"_"+self.abbr+"_"+str(self.pk)
    
class ZellaUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=10, unique=True)
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    email = models.EmailField(max_length=75)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'email' ]

    objects = ZellaUserManager()

    def first_name(self):
        return self.firstname
    
    def last_name(self):
        return self.lastname

    def __str__(self):
        return self.firstname+" "+self.lastname

class Quiz(models.Model):
    title = models.CharField(max_length=75)
    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField('Due Date', blank=False)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text
    
class UnitRegistration(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    student = models.ForeignKey(ZellaUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.unit
    
class AssignmentSubmission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(ZellaUser, on_delete=models.CASCADE)
    score = models.PositiveBigIntegerField(null=True, blank=True)