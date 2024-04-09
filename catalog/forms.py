from django import forms
from .models import Message


class AddMessageForm(forms.Form):
    name = forms.CharField(max_length=80, widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Введите имя'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control', 'placeholder':'Введите почту'}))
    subject = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class':'form-control', 'placeholder':'Введите название темы'}))
    body = forms.Textarea(attrs={
        'class':'form-control', 'placeholder':'Введите сообщение'})
    class Meta:
        model = Message
        fields = ('name', 'email', 'subject', 'body')
