from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ZellaUser

class ZellaUserCreationForm(UserCreationForm):

    class Meta:
        model = ZellaUser
        fields = ('firstname', 'lastname', 'email', 'course')

class ZellaUserChangeForm(UserChangeForm):

    class Meta:
        model = ZellaUser
        fields = ('firstname', 'lastname', 'email')