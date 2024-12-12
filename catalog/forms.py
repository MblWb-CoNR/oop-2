from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import AdvUser
from .models import Application
from .models import Categories
from django.core.validators import RegexValidator


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты', validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                message=' Необходим валидный формат email-адреса'
            )
        ])
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Пароль (повторно)',
        widget=forms.PasswordInput,help_text='Повторите тот же самый пароль еще раз'
    )
    first_name = forms.CharField(label='Имя', max_length=100, validators=[
            RegexValidator(
                regex=r'^[а-яА-ЯёЁ\s-]+$',
                message='Имя должно состоять только из кириллических букв, пробелов и дефисов.'
            )
        ])
    patronymic = forms.CharField(label='Отчество', max_length=100, validators=[
            RegexValidator(
                regex=r'^[а-яА-ЯёЁ-]+$',
                message='Отчество должно состоять только из кириллических букв и дефисов.'
            )
        ])
    last_name = forms.CharField(label='Фамилия', max_length=100, validators=[
            RegexValidator(
                regex=r'^[а-яА-ЯёЁ-]+$',
                message='Фамилия должно состоять только из кириллических букв и дефисов.'
            )
        ])
    username = forms.CharField(label='Логин', max_length=30, validators=[
            RegexValidator(
                regex=r'^[a-zA-Z-]+$',
                message='Логин должен состоять только из латинских букв и дефисов.'
            )
        ])
    consent = forms.BooleanField(label='Согласие на обработку персональных данных')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()  #встроенная функция, которая позволяет вызывать методы родительского класса
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', ValidationError(
                'Введенные пароли не совпадают.'
            ))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'first_name', 'patronymic', 'last_name', 'email', 'password1',
                  'password2', 'tariff', 'consent')


class ApplicationForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Categories.objects.all(),
    )
    class Meta:
        model = Application
        fields = ('name', 'description', 'categories', 'photo', 'price')

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Размер фото не должен превышать 2 Мб.")
        return photo

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        application = super().save(commit=False)
        application.user = self.user

        if self.user.tariff == 'company':
            multiplier = 1.20
        elif self.user.tariff == 'individual':
            multiplier = 1.06
        else:
            multiplier = 1.00

        base_price = 10000
        application.price = base_price * multiplier

        if commit:
            application.save()
            self.save_m2m()
        return application