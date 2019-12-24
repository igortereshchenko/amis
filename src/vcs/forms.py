from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class StudentLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class LectureCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)


class PredictScoreForm(forms.Form):
    views = forms.IntegerField(max_value=50, min_value=0)
    comments = forms.IntegerField(max_value=50, min_value=0)
    likes = forms.IntegerField(max_value=50, min_value=0)
