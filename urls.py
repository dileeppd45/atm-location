from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('home_page', views.home_page, name="home_page"),
    path('login',views.login, name='login'),
    path('signin_branch',views.signin_branch, name='signin_branch'),
    path('signin',views.signin, name='signin'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('approved_branches', views.approved_branches, name='approved_branches'),
    path('admin_view_branchwise_atm/<str:id>', views.admin_view_branchwise_atm, name='admin_view_branchwise_atm'),
    path('pending_branches', views.pending_branches, name='pending_branches'),
    path('approve_branch/<str:id>', views.approve_branch, name='approve_branch'),
    path('branch_home', views.branch_home, name='branch_home'),
    path('add_atm', views.add_atm, name='add_atm'),
    path('view_atm', views.view_atm, name='view_atm'),
    path('open_atm/<int:id>', views.open_atm, name='open_atm'),
    path('close_atm/<str:id>', views.close_atm, name='close_atm'),
    path('profile', views.profile, name='profile'),
    path('change_password', views.change_password, name='change_password'),
    path('change_password_user', views.change_password_user, name='change_password_user'),
    path('update_password', views.update_password, name='update_password'),
    path('update_password_user', views.update_password_user, name='update_password_user'),
    path('user_home', views.user_home, name='user_home'),
    path('location/<str:id>/<str:jd>',views.location, name='location'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('user_view_bank', views.user_view_bank, name='user_view_bank'),
    path('user_view_branch/<str:id>', views.user_view_branch, name='user_view_branch'),
    path('user_view_branchwise_atm/<str:id>', views.user_view_branchwise_atm, name='user_view_branchwise_atm'),

]

