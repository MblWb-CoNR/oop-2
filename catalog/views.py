from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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
from .forms import ApplicationAdminForm
from .models import Application


def index(request):
    num_application_in_work = Application.objects.filter(status__exact='o').count()
    applications = Application.objects.filter(status__exact='d').order_by('-date')[:4]
    return render(
        request,
        'index.html',
        context={'num_application_in_work': num_application_in_work, 'applications': applications})


class BBLoginView(LoginView):
    template_name = 'registration/login.html'


@login_required
def profile(request):
    applications = Application.objects.filter(user=request.user)
    return render(request, 'registration/profile.html', {'applications': applications})


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logout.html'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('catalog:register_done')

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     user = self.object
    #
    #     subject = 'Регистрация на сайте'
    #     message = f'Спасибо за регистрацию! Вы выбрали тариф: {dict(form.TARIFF_CHOICES)[tariff]}'
    #     from_email = 'malenkoer@mail.ru'
    #     recipient_list = [user.email]
    #     send_mail(subject, message, from_email, recipient_list)
    #
    #     try:
    #         send_mail(subject, message, from_email, recipient_list)
    #     except Exception as e:
    #         print(f'Email sending failed: {e}')
    #
    #     login(self.request, user)
    #     return response


class RegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'


@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            application = form.save()
            return redirect('catalog:profile')
    else:
        form = ApplicationForm(user=request.user)
    return render(request, 'application/create_application.html', {'form': form})


@login_required
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, user=request.user)

    if application.user != request.user:
        messages.error(request, "У вас нет прав на удаление этой заявки.")
        return redirect('catalog:profile')

    if application.status != 'n':  # 'n' - статус "Новая"
        messages.error(request, "Заявку нельзя удалить, так как её статус изменён.")
        return redirect('catalog:profile')

    if request.method == 'POST':
        application.delete()
        return redirect('catalog:profile')

    return render(request, 'application/delete_application.html', {'application': application})


@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if request.method == 'POST':
        form = ApplicationAdminForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            application = form.save(commit=False)
            if application.status == 'd' and not application.photo:
                form.add_error('photo', 'Необходимо загрузить фотографию для заявки со статусом "Выполнена"')
            elif application.status == 'o' and not application.comment:
                form.add_error('comment', 'Необходимо добавить комментарий для заявки со статусом "Принята в работу"')
            else:
                application.save()
                return redirect('catalog:profile')
    else:
        form = ApplicationAdminForm(instance=application)
    return render(request, 'application/edit_application.html', {'form': form, 'application': application})


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_profile(request):
    applications = Application.objects.all()
    return render(request, 'registration/admin_profile.html', {'applications': applications})