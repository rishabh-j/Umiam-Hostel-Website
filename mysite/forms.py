from django import forms
from django.contrib.auth.models import User
from .models import About,Award,Announcement,Doctake,Boarder,Filler,Note,Messmenu,Canteenmenu
from .choices import *
import datetime
from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime
date_range = 100    
this_year = datetime.now().year
from django.forms import extras
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']

class AboutForm(forms.ModelForm):
    birth_date= forms.DateField(widget=extras.SelectDateWidget(years=range(this_year - date_range, this_year)))
    class Meta:
        model = About
        fields = ['name','birth_date','position', 'dept','image','email','telephone','roomnumber','authentication_key']

class AnnouncementForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = ['info','title','date']

class AwardForm(forms.ModelForm):

    class Meta:
        model = Award
        fields = ['detail','position','year']

class DocForm(forms.ModelForm):
    hostel = forms.ChoiceField(choices = HOSTEL_CHOICES, required=True)
    class Meta:
        model = Doctake
        fields = ['doc','hostel']

class BoarderForm(forms.ModelForm):

    class Meta:
        model = Boarder
        fields = ['name','roomnumber','rollnumber','dept','telephone']

class FillerForm(forms.ModelForm):

    class Meta:
        model = Filler
        fields = ['name','phonenumber','hostel']


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields= ['material','year','Course_code']

class MessmenuForm(forms.ModelForm):

    class Meta:
        model=Messmenu
        fields = ['image','date']

class CanteenmenuForm(forms.ModelForm):

    class Meta:
        model=Canteenmenu
        fields = ['image','date']
