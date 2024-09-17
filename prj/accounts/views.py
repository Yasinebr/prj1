from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'user create successfully', 'success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})

class LoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'username or password is wring', 'warning')
        return render(request, self.template_name, {'form':form})

class LogoutView(LoginRequiredMixin ,View):
    def get(self, request):
        logout(request)
        messages.success(request, 'logout successfully', 'success')
        return redirect('home:home')

class ProfileView(LoginRequiredMixin ,View):
    def get(self, request ,user_id):
        user = User.objects.get(pk=user_id)
        return render(request, 'accounts/profile.html', {'user':user})