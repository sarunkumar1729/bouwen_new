from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('courses', views.courses, name='courses'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('login', views.user_login, name='login'),
    path('python', views.python, name='python'),
    path('adminindex',views.admin_index,name='adminindex'),
    path('adminlogin',views.admin_login,name='adminlogin'),
    path('jobs',views.jobs,name='jobs'),
    path('editprofile',views.edit_profile,name='editprofile'),
    path('profile',views.profile,name='profile'),
    path('candidates',views.users_list,name='candidates'),
    path('userlogout',views.user_logout,name='userlogout'),
    path('jobsavailable',views.jobs_available,name='jobsavailable'),
    path('applyjob/<int:i>',views.apply_job,name='applyjob'),
    path('userprofile/<int:i>',views.user_profile,name='userprofile'),
    path('verify1',views.verify1,name='verify1'),
    path('verify2',views.verify2,name='verify2'),
]
