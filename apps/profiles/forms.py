# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext
from django.forms.models import inlineformset_factory
from django.contrib.gis import admin
from django.contrib.auth import authenticate
from django.contrib.auth import login

from profiles.models import Profile
from maap.models import MaapPoint
from maap.forms import InlinePointForm


class LoginForm(forms.Form):

    username = forms.CharField(
        label=_("Nombre de usuario"), 
        max_length=30,
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label=_("Password"), 
        widget=forms.PasswordInput(render_value=False)
    )
    remember = forms.BooleanField(
        label=_("Recordarme"), 
        help_text=_("No cerrar la cuenta por tres semanas"), 
        required=False
    )

    user = None

    def clean(self):
        if self._errors:
            return
        user = authenticate(
            username=self.cleaned_data["username"], 
            password=self.cleaned_data["password"]
        )
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(_("Esta cuenta es inactiva"))
        else:
            raise forms.ValidationError(_("El nombre de usuario o password no son correctos"))
        return self.cleaned_data

    def login(self, request):
        if self.is_valid():
            login(request, self.user)
            request.user.message_set.create(message=ugettext(u"Bienvenido"))
            if self.cleaned_data['remember']:
                request.session.set_expiry(60 * 60 * 24 * 7 * 3)
            else:
                request.session.set_expiry(0)
            return True
        return False


class ProfileForm(forms.ModelForm):
    description = forms.CharField(label = 'Mensaje', widget=forms.Textarea(attrs={'cols':60}))
    class Meta:
        model = Profile
        exclude = ('user','location')

class MailForm(forms.Form):
    name = forms.CharField(label = 'Su nombre', max_length = 50)
    mail = forms.EmailField(label = 'Su email')
    message = forms.CharField(label = 'Mensaje', widget=forms.Textarea)

