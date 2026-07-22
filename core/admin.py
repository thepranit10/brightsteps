from django.contrib import admin
from .models import Homework, EventPhoto, Student, Teacher, ClassSchedule, Attendance, SchoolNotice, CalendarEvent, Lesson, QuizQuestion

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'subject', 'grade_level', 'created_at')
    list_filter = ('subject', 'grade_level')
    search_fields = ('title_en', 'title_mr', 'description_en', 'description_mr')

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_en', 'subject', 'grade_level', 'points', 'created_at')
    list_filter = ('subject', 'grade_level')
    search_fields = ('question_en', 'question_mr')

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'due_date', 'created_at')
    list_filter = ('subject', 'due_date')
    search_fields = ('title', 'description', 'subject')

@admin.register(EventPhoto)
class EventPhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'photo')
    search_fields = ('title',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'grade_level', 'total_stars', 'joined_date')
    list_filter = ('grade_level', 'joined_date')
    search_fields = ('name', 'roll_number', 'email')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject_specialty', 'assigned_class', 'joined_date')
    list_filter = ('assigned_class', 'subject_specialty')
    search_fields = ('name', 'email', 'subject_specialty')

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ('subject', 'day_of_week', 'start_time', 'end_time', 'teacher')
    list_filter = ('day_of_week', 'subject')
    search_fields = ('subject', 'teacher__name')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('student__name', 'student__roll_number')

@admin.register(SchoolNotice)
class SchoolNoticeAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'date', 'author_name', 'is_urgent')
    list_filter = ('is_urgent', 'date')
    search_fields = ('title_en', 'title_mr', 'content_en', 'content_mr')

@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'date', 'time', 'color_hex')
    list_filter = ('date',)
    search_fields = ('title_en', 'title_mr', 'description_en', 'description_mr')

