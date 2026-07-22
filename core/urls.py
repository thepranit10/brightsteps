from django.urls import path
from . import views

urlpatterns = [
    path('', views.public_home, name='home_page'),
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('homework/', views.homework_list, name='homework_list'),
    path('homework/add/', views.homework_create, name='homework_create'),
    path('homework/<uuid:pk>/edit/', views.homework_edit, name='homework_edit'),
    path('homework/<uuid:pk>/delete/', views.homework_delete, name='homework_delete'),

    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/upload-csv/', views.student_upload_csv, name='student_upload_csv'),
    path('students/<uuid:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<uuid:pk>/delete/', views.student_delete, name='student_delete'),

    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.teacher_create, name='teacher_create'),
    path('teachers/<uuid:pk>/edit/', views.teacher_edit, name='teacher_edit'),
    path('teachers/<uuid:pk>/delete/', views.teacher_delete, name='teacher_delete'),

    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.attendance_create, name='attendance_create'),

    path('schedule/', views.schedule_list, name='schedule_list'),
    path('schedule/add/', views.schedule_create, name='schedule_create'),
    
    path('events/', views.event_photo_list, name='event_photo_list'),
    path('events/add/', views.event_photo_create, name='event_photo_create'),

    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/add/', views.lesson_create, name='lesson_create'),
    path('lessons/<uuid:pk>/edit/', views.lesson_edit, name='lesson_edit'),
    path('lessons/<uuid:pk>/delete/', views.lesson_delete, name='lesson_delete'),

    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/add/', views.quiz_create, name='quiz_create'),
    path('quizzes/<uuid:pk>/edit/', views.quiz_edit, name='quiz_edit'),
    path('quizzes/<uuid:pk>/delete/', views.quiz_delete, name='quiz_delete'),

    # School Notices
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/add/', views.notice_create, name='notice_create'),
    path('notices/<uuid:pk>/delete/', views.notice_delete, name='notice_delete'),

    # Calendar Events
    path('calendar/', views.event_list, name='event_list'),
    path('calendar/add/', views.event_create, name='event_create'),
    path('calendar/<uuid:pk>/delete/', views.event_delete, name='event_delete'),
]
