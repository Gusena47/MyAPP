from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView
import datetime
from myauth.models import Profile
from .forms import ProfileUpdateForm,UserUpdateForm

# для урока 13.3
from django.utils.translation import gettext as _
# конец

# для урока 13.3
class HelloView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        welcome_mess = _('Hello world')
        return HttpResponse(f'<h1>{welcome_mess}</h1>')
# конец

class AboutMeView(TemplateView):
    template_name = 'myauth/about_me.html'


class UsersListView(ListView):
    # model = Profile
    context_object_name = 'profiles'
    template_name = 'myauth/users_list.html'
    queryset = (
        Profile.objects
        .select_related("user"))

class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'myauth/profile_detail.html'

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name ='myauth/register.html'
    success_url = reverse_lazy('myauth:about')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)
        return response


def login_view(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin')

        return render(request,'myauth/login.html')

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin')

    return render(request, 'myauth/login.html', {'error': 'Invalid login'})

class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth/login')


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'myauth/profile_edit.html'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        if all([form.is_valid(), user_form.is_valid()]):
            user_form.save()
            form.save()
        else:
            context.update({'user_form': user_form})
            return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('myauth:about')

# def logout_view(request: HttpRequest):
#     logout(request)
#     return redirect(reverse('myauth/login'))

def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fuxx', 'buzz', max_age=3600)
    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fuxx', 'default value')
    return HttpResponse(f'Cookie value: {value}')

@permission_required('yauth.view_profile', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spasae'
    return HttpResponse('Session set!')

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default value')
    return HttpResponse(f'Session value {value}')

class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar'})
