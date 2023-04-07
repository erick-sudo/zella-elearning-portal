from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import College, Course, Unit, Quiz, Question, Choice, ZellaUser

from .forms import ZellaUserCreationForm, ZellaUserChangeForm


# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice

class QuestionInline(admin.TabularInline):
    model = Question
    fieldsets = [
        ('Question', {'fields': ['question_text']})
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date' )

class QuizAdmin(admin.ModelAdmin):
    model = Quiz
    fieldsets = [
        ('Quiz', {"fields": ['title', 'unit', 'due_date']}),
    ]
    list_display= ['title', 'unit', 'due_date']
    classes = ['collapse']
    inlines = [QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    fieldsets = [
        ('Question', {'fields': ['question_text', 'quiz']}),
    ]
    list_display = ['question_text', 'pub_date', 'quiz']
    inlines = [ChoiceInline]


class ZellaUserAdmin(UserAdmin):
    add_form = ZellaUserCreationForm
    form = ZellaUserChangeForm
    model = ZellaUser
    list_display = ('firstname', 'lastname', 'email', 'course', 'is_staff', 'is_active')
    fieldsets = (
        ("Modify User", {"fields": ("firstname", "lastname", "username", "email", "course")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        ("Create New User", {
            "classes": ("wide",),
            "fields": (
                "username", "firstname","lastname", "email", "course", "is_staff", 
                "is_active", "password1", "password2", "groups", "user_permissions"
            )}
        ),
    )


admin.site.register(College)
admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)

admin.site.register(ZellaUser, ZellaUserAdmin)