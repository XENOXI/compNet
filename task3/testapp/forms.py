from django import forms

class UserForm(forms.Form):
    link = forms.CharField()
    login = forms.CharField()
    password = forms.CharField()
    first_semester = forms.IntegerField()
    last_semester = forms.IntegerField()

class SendForm(forms.Form):
    file = forms.FileField()
        