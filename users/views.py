from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView

from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/account_settings.html'
    form_class = UserUpdateForm

    success_url = reverse_lazy('user_update')
    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        # Смотрим, какая именно форма была отправлена
        form_type = request.POST.get('form_type')

        # Если это форма профиля -> пусть UpdateView работает как обычно
        if form_type == 'profile_update':
            return super().post(request, *args, **kwargs)

        # Если это форма пароля -> включаем нашу ручную логику
        elif form_type == 'password_update':
            user = request.user
            current_pass = request.POST.get('current_password')
            new_pass = request.POST.get('new_password')
            confirm_pass = request.POST.get('confirm_password')

            # 1. Проверяем старый пароль
            if not user.check_password(current_pass):
                messages.error(request, 'Текущий пароль введен неверно.')

            # 2. Проверяем, совпадают ли новые пароли
            elif new_pass != confirm_pass:
                messages.error(request, 'Новые пароли не совпадают.')

            # 3. Если всё ок — сохраняем
            else:
                user.set_password(new_pass)
                user.save()

                # ВАЖНО: Эта функция не даст Джанго разлогинить тебя после смены пароля
                update_session_auth_hash(request, user)
                messages.success(request, 'Ваш пароль успешно изменен!')
        elif form_type == 'delete_account':
            user = request.user
            # Сначала обязательно разлогиниваем (удаляем сессию)
            logout(request)
            # Затем удаляем самого пользователя из базы данных
            user.delete()

            # Добавляем сообщение (оно покажется на главной странице)
            messages.success(request, 'Ваш аккаунт был навсегда удален. Нам будет вас не хватать!')

            # Отправляем на главную страницу форума
            return redirect('index')
            # Перезагружаем страницу настроек
            return redirect('user_update')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_.html'
    form_class = UserRegisterForm


def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            print("ОШИБКИ ФОРМЫ:", form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def user_account(request):
    total_likes = 0
    user_posts = request.user.articles_set.all()
    for article in request.user.articles_set.all():
        total_likes += article.likes.count()
    context = {'total_likes': total_likes, 'user_posts': user_posts}
    return render(request, 'users/user_account.html', context)




