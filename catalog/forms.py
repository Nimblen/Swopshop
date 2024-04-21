from unicodedata import category
from django import forms
from .models import Message, Item, Category, Photo_of_item


class AddMessageForm(forms.Form):
    name = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите имя"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите почту"}
        )
    )
    subject = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите название темы"}
        ),
    )
    body = forms.Textarea(
        attrs={"class": "form-control", "placeholder": "Введите сообщение"}
    )

    class Meta:
        model = Message
        fields = ("name", "email", "subject", "body")


class AddItemForm(forms.ModelForm):
    name = forms.CharField(
        max_length=80,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите название"}
        ),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Введите описание"}
        )
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={"class": "custom-select"}),
    )
    choices = (("service", "Услуга"), ("item", "Вещь"))
    type = forms.ChoiceField(choices=choices, initial="item")

    class Meta:
        model = Item
        fields = ("name", "description", "category", "type")


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo_of_item
        fields = ["photo"]


PhotoFormSet = forms.inlineformset_factory(
    Item,
    Photo_of_item,
    form=PhotoForm,
    extra=3,
    can_delete=False,
)
