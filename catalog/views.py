from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AdvUser
from django.views.generic import CreateView
from .forms import RegisterUserForm
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.core.mail import send_mail
from django.contrib.auth import login
from .forms import ApplicationForm


def index(request):
    return render(request, 'index.html')


class BBLoginView(LoginView):
    template_name = 'registration/login.html'


@login_required
def profile(request):
    return render(request, 'registration/profile.html')


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logout.html'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('catalog:register_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        tariff = form.cleaned_data.get('tariff')

        subject = 'Регистрация на сайте'
        message = f'Спасибо за регистрацию! Вы выбрали тариф: {dict(form.TARIFF_CHOICES)[tariff]}'
        from_email = 'malenkoer@mail.ru'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print(f'Email sending failed: {e}')

        login(self.request, user)
        return response


class RegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'


def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ApplicationForm()

    return render(request, 'application/create_application.html', {'form': form})


