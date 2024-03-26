from django.urls import path
from django.contrib.auth.views import LoginView

from .views import HelloView, MyLogoutView, AboutMeView, ProfileUpdateView, ProfileDetailView, \
    UsersListView, RegisterView, get_cookie_view, set_cookie_view, get_session_view, set_session_view, FooBarView

app_name = 'myauth'

urlpatterns = [
    path('', LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('hello/', HelloView.as_view(), name='hello'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('about_me/', AboutMeView.as_view(), name='about'),
    path('about_me/edit', ProfileUpdateView.as_view(), name='about_edit'),
    path('users/<int:pk>',ProfileDetailView.as_view(), name='profile'),
    path('users/', UsersListView.as_view(), name='users'),
    path('register/', RegisterView.as_view(), name='register'),
    path('cookie/get/', get_cookie_view, name='cookie-get'),
    path('cookie/set/', set_cookie_view, name='cookie-set'),
    path('session/get/', get_session_view, name='session-get'),
    path('session/set/', set_session_view, name='session-set'),
    path('foo-bar/', FooBarView.as_view(), name='foo-bar'),
]
