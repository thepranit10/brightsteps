from django.db import models
import uuid
from .storage import SupabaseStorage

class Homework(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=100)
    due_date = models.DateField()
    attachment = models.FileField(upload_to='', storage=SupabaseStorage(), null=True, blank=True)
    teacher_id = models.UUIDField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'homework'

    def __str__(self):
        return f"{self.title} ({self.subject})"

class Student(models.Model):
    CLASS_CHOICES = [
        ('Jr KG', 'Jr KG'),
        ('Sr KG', 'Sr KG'),
        ('Class 1', 'Class 1'),
        ('Class 2', 'Class 2'),
        ('Class 3', 'Class 3'),
        ('Class 4', 'Class 4'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    parent_phone_number = models.CharField(max_length=15, null=True, blank=True, help_text="Used for parent login. Siblings can share the same number.")
    roll_number = models.CharField(max_length=50, unique=True)
    grade_level = models.CharField(max_length=50, choices=CLASS_CHOICES)
    joined_date = models.DateField(auto_now_add=True)
    total_stars = models.IntegerField(default=0)
    lessons_completed = models.IntegerField(default=0)
    quizzes_taken = models.IntegerField(default=0)
    average_quiz_score = models.IntegerField(default=0)
    badges = models.TextField(blank=True, null=True, help_text="Comma-separated list of badges, e.g. 'b1,b3'")


    class Meta:
        db_table = 'student'

    def __str__(self):
        return f"{self.name} ({self.grade_level})"

class Teacher(models.Model):
    CLASS_CHOICES = [
        ('Jr KG', 'Jr KG'),
        ('Sr KG', 'Sr KG'),
        ('Class 1', 'Class 1'),
        ('Class 2', 'Class 2'),
        ('Class 3', 'Class 3'),
        ('Class 4', 'Class 4'),
        ('All Classes', 'All Classes'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    subject_specialty = models.CharField(max_length=100)
    assigned_class = models.CharField(max_length=50, choices=CLASS_CHOICES, default='Class 1')
    joined_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'teacher'

    def __str__(self):
        return f"{self.name} ({self.assigned_class})"

class ClassSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    day_of_week = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = 'class_schedule'

    def __str__(self):
        return f"{self.subject} - {self.day_of_week}"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        db_table = 'attendance'
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.date} ({self.status})"

class EventPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, help_text="Optional title for the photo")
    photo = models.FileField(upload_to='', storage=SupabaseStorage(bucket_name='events_photos'))
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'event_photo'
        verbose_name_plural = 'Event Photos'

    def __str__(self):
        return self.title or f"Event Photo {self.id}"

class SchoolNotice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title_mr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    content_mr = models.TextField()
    content_en = models.TextField()
    date = models.DateField(auto_now_add=True)
    author_name = models.CharField(max_length=100)
    is_urgent = models.BooleanField(default=False)

    class Meta:
        db_table = 'school_notice'

    def __str__(self):
        return self.title_en

class CalendarEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title_mr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    date = models.DateField()
    time = models.CharField(max_length=50)
    description_mr = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    color_hex = models.CharField(max_length=7, default='#3B82F6')

    class Meta:
        db_table = 'calendar_event'

    def __str__(self):
        return self.title_en

class Lesson(models.Model):
    SUBJECT_CHOICES = [
        ('Marathi', 'Marathi'),
        ('English', 'English'),
        ('Mathematics', 'Mathematics'),
        ('Rhymes', 'Rhymes'),
        ('Stories', 'Stories'),
        ('Videos', 'Videos'),
    ]
    GRADE_CHOICES = [
        ('Jr KG', 'Jr KG'),
        ('Sr KG', 'Sr KG'),
        ('Class 1', 'Class 1'),
        ('Class 2', 'Class 2'),
        ('Class 3', 'Class 3'),
        ('Class 4', 'Class 4'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    grade_level = models.CharField(max_length=50, choices=GRADE_CHOICES, default='Class 1')
    title_mr = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    description_mr = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    content_mr = models.TextField(blank=True, null=True)
    content_en = models.TextField(blank=True, null=True)
    icon_res = models.CharField(max_length=100, blank=True, null=True)
    color_hex = models.CharField(max_length=7, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lesson'

    def __str__(self):
        return f"{self.title_en} ({self.subject} - {self.grade_level})"

class QuizQuestion(models.Model):
    SUBJECT_CHOICES = [
        ('Marathi', 'Marathi'),
        ('English', 'English'),
        ('Mathematics', 'Mathematics'),
    ]
    GRADE_CHOICES = [
        ('Jr KG', 'Jr KG'),
        ('Sr KG', 'Sr KG'),
        ('Class 1', 'Class 1'),
        ('Class 2', 'Class 2'),
        ('Class 3', 'Class 3'),
        ('Class 4', 'Class 4'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    grade_level = models.CharField(max_length=50, choices=GRADE_CHOICES, default='Class 1')
    question_mr = models.TextField()
    question_en = models.TextField()
    option_1_en = models.CharField(max_length=255)
    option_2_en = models.CharField(max_length=255)
    option_3_en = models.CharField(max_length=255)
    option_4_en = models.CharField(max_length=255)
    option_1_mr = models.CharField(max_length=255)
    option_2_mr = models.CharField(max_length=255)
    option_3_mr = models.CharField(max_length=255)
    option_4_mr = models.CharField(max_length=255)
    correct_answer_index = models.IntegerField()
    points = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quiz_question'

    def __str__(self):
        return f"{self.question_en[:50]}... ({self.subject} - {self.grade_level})"


