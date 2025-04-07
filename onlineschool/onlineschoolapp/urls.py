from django.urls import path, include
from django.conf import settings
# from . import views
from onlineschoolapp import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('courses/<int:pk>', views.CourseDetailView.as_view(), name='course_detail'),
    path('teachers/', views.TeacherListView.as_view(), name='teachers'),
    path('teachers/<int:pk>', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('mentors/', views.MentorListView.as_view(), name='mentors'),
    path('mentors/<int:pk>', views.MentorDetailView.as_view(), name='mentor_detail'),
    path('students/', views.StudentListView.as_view(), name='students'),
    path('students/<int:pk>', views.StudentDetailView.as_view(), name='student_detail'),
    path('lessons/', views.LessonListView.as_view(), name='lessons'),
    path('lessons/<int:pk>', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('mygrades/', views.StudentGradesListView.as_view(), name='grades'),
    path('lessons/create/', views.LessonCreate.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/delete/', views.LessonDelete.as_view(), name='lesson_delete'),
    path('grades/<int:pk>/update/', views.GradeUpdate.as_view(), name='grades_update'),
    path('lectures/create/', views.LectureCreate.as_view(), name='lecture_create'),
    path('quizzes/create/', views.QuizCreate.as_view(), name='quiz_create'),
    #path('quizzes/<int:quiz_id>/results/', views.QuizResultsView.as_view(), name='quiz_results'),
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('quizzes/<int:pk>/take/', views.TakeQuizView.as_view(), name='take_quiz'),
    path('quizzes/<int:pk>/submit/', views.SubmitQuizView.as_view(), name='submit_quiz'),
    path('quizzes/<int:pk>/results/', views.QuizResultsView.as_view(), name='quiz_results'),
    path('quizzes/<int:pk>/questions/create/', views.QuestionCreate.as_view(), name='question_create'),
    path('lectures/<int:pk>/', views.LectureDetailView.as_view(), name='lecture_detail'),   # добавить вывод всех лекций преподавателя
    path('lectures/create/', views.LectureCreate.as_view(), name='lecture_create'),
    path('student/lectures/', views.StudentLecturesView.as_view(), name='student_lectures'),
    path('lectures/<int:pk>/update/', views.LectureUpdate.as_view(), name='lecture_update'),
    path('quizzes/create/', views.QuizCreate.as_view(), name='quiz_create'),
    # path('quizzes/<int:pk>/', views.TakeQuizView.as_view(), name='take_quiz'),
    path('quizzes/<int:pk>/results/', views.QuizResultsView.as_view(), name='quiz_results'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('my-lectures/', views.TeacherLecturesView.as_view(), name='teacher_lectures'),
    path('quizzes/<int:quiz_id>/student/<int:student_id>/', views.StudentQuizDetailsView.as_view(), name='student_quiz_details'),
    path('lecture/<int:pk>/delete/', views.LectureDelete.as_view(), name='lecture_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
