from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=25)
    password = forms.CharField(widget=forms.PasswordInput, label="password", max_length=32)

    template_name = "components/form.html"
