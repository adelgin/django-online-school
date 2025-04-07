from django.contrib import admin
from django.urls import path, include
from onlineschoolapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('onlineschoolapp.urls')),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/student/', views.StudentSignUpView.as_view(), name='student_signup'),
    path('signup/teacher/', views.TeacherSignUpView.as_view(), name='teacher_signup'),
    path('signup/mentor/', views.MentorSignUpView.as_view(), name='mentor_signup'),
]
