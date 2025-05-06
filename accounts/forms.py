from allauth.account.forms import LoginForm as AllauthLoginForm
from allauth.account.forms import SignupForm as AllauthSignupForm
from django import forms
from django.utils.translation import gettext_lazy as _


class LoginForm(AllauthLoginForm):
    """Форма логина по email + password"""

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["login"].label = _("Email")
        self.fields["login"].widget = forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "your@email.com"}
        )
        self.fields["password"].widget = forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "••••••••"}
        )
        self.fields["remember"].widget.attrs.update({"class": "form-check-input"})


class SignupForm(AllauthSignupForm):
    """Форма регистрации с полным именем"""

    full_name = forms.CharField(
        label="Полное имя",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваше полное имя"}),
    )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget = forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        )
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Пароль"}
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Подтвердите пароль"}
        )

    def save(self, request):
        user = super(SignupForm, self).save(request)
        user.first_name = self.cleaned_data["full_name"]
        user.save()
        return user
