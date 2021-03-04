from account import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView



urlpatterns = [

	path("signin",views.user_login,name="user_login"),
   	path("signup/",views.register,name="signup"),
	path("check_user/",views.check_user,name="check_user"),
	path("user_logout/",views.user_logout,name="user_logout"),
	path("edit_profile/",views.edit_profile,name="edit_profile"),
	path("change_password/",views.change_password,name="change_password"),
	#path("forgotpass",views.forgotpass, name="forgotpass"),
    #path("reset_password",views.reset_password,name="reset_password"),
   	
   	path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='account/commons/password-reset/password_reset.html',
             subject_template_name='account/commons/password-reset/password_reset_subject.txt',
             email_template_name='account/commons/password-reset/password_reset_email.html',
             success_url='/account/user_login'
         ),
         name='password_reset'),
    

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/commons/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/commons/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/commons/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]


