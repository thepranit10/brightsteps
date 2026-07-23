import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Homework, Lesson, QuizQuestion, Student, Teacher, ClassSchedule, Attendance, EventPhoto, SchoolNotice, CalendarEvent

def public_home(request):
    today = datetime.date.today()
    notices = SchoolNotice.objects.all().order_by('-date')[:4]
    upcoming_events = CalendarEvent.objects.filter(date__gte=today).order_by('date')[:4]
    event_photos = EventPhoto.objects.all().order_by('-uploaded_at')[:6]
    teachers = Teacher.objects.all()[:6]
    total_students = Student.objects.count()
    total_lessons = Lesson.objects.count()
    
    classes_list = [
        {'name': 'Jr KG', 'desc': 'Foundational Marathi & English vowels recognition, number counting & nursery rhymes', 'icon': 'fa-child'},
        {'name': 'Sr KG', 'desc': 'Consonant recognition, color names, counting objects & fun story telling', 'icon': 'fa-shapes'},
        {'name': 'Class 1', 'desc': 'Simple Marathi words, English 3-letter spelling, basic addition & subtraction', 'icon': 'fa-book-open'},
        {'name': 'Class 2', 'desc': 'Sentence reading, numbers up to 100, story comprehension & quizzes', 'icon': 'fa-calculator'},
        {'name': 'Class 3', 'desc': 'Advanced Marathi grammar, multiplication tables, science & general knowledge', 'icon': 'fa-brain'},
        {'name': 'Class 4', 'desc': 'Comprehensive primary curriculum, interactive quizzes & exam preparation', 'icon': 'fa-award'},
    ]
    
    context = {
        'notices': notices,
        'upcoming_events': upcoming_events,
        'event_photos': event_photos,
        'teachers': teachers,
        'classes_list': classes_list,
        'total_students': total_students,
        'total_lessons': total_lessons,
    }
    return render(request, 'home.html', context)

def about_view(request):
    return render(request, 'about.html')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next')
            return redirect(next_url if next_url else 'dashboard_home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
            
    return render(request, 'login.html')


def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def dashboard_home(request):
    total_homework = Homework.objects.count()
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_lessons = Lesson.objects.count()
    total_quizzes = QuizQuestion.objects.count()
    subjects_count = Homework.objects.values('subject').distinct().count()
    
    # Class standard breakdown
    classes_list = ['Jr KG', 'Sr KG', 'Class 1', 'Class 2', 'Class 3', 'Class 4']
    class_breakdown = []
    for c in classes_list:
        s_count = Student.objects.filter(grade_level=c).count()
        teachers = Teacher.objects.filter(assigned_class__icontains=c)
        teacher_names = ", ".join([t.name for t in teachers]) if teachers.exists() else "No Teacher Assigned"
        class_breakdown.append({
            'name': c,
            'students': s_count,
            'teachers': teacher_names,
        })

    # Recent Data
    recent_homework = Homework.objects.all().order_by('-created_at')[:4]
    recent_students = Student.objects.all().order_by('-joined_date')[:4]
    
    # Dynamic School Notices & Calendar Events
    today = datetime.date.today()
    notices = SchoolNotice.objects.all().order_by('-date')[:5]
    upcoming_events = CalendarEvent.objects.filter(date__gte=today).order_by('date')[:5]
    
    context = {
        'total_homework': total_homework,
        'subjects_count': subjects_count if subjects_count > 0 else 5,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_lessons': total_lessons,
        'total_quizzes': total_quizzes,
        'class_breakdown': class_breakdown,
        'recent_homework': recent_homework,
        'recent_students': recent_students,
        'notices': notices,
        'upcoming_events': upcoming_events,
        'today_date': today.strftime("%B %d, %Y"),
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='/login/')
def homework_list(request):
    homeworks = Homework.objects.all().order_by('-created_at')
    return render(request, 'homework_list.html', {'homeworks': homeworks})

@login_required(login_url='/login/')
def homework_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        subject = request.POST.get('subject')
        due_date = request.POST.get('due_date')
        description = request.POST.get('description')
        attachment = request.FILES.get('attachment')
        
        Homework.objects.create(
            title=title,
            subject=subject,
            due_date=due_date,
            description=description,
            attachment=attachment
        )
        return redirect('homework_list')
        
    return render(request, 'homework_form.html', {'action_title': 'Add'})

@login_required(login_url='/login/')
def homework_edit(request, pk):
    homework = get_object_or_404(Homework, pk=pk)
    
    if request.method == 'POST':
        homework.title = request.POST.get('title')
        homework.subject = request.POST.get('subject')
        homework.due_date = request.POST.get('due_date')
        homework.description = request.POST.get('description')
        
        if 'attachment' in request.FILES:
            homework.attachment = request.FILES.get('attachment')
            
        homework.save()
        return redirect('homework_list')
        
    return render(request, 'homework_form.html', {'action_title': 'Edit', 'homework': homework})

@login_required(login_url='/login/')
def homework_delete(request, pk):
    homework = get_object_or_404(Homework, pk=pk)
    if request.method == 'POST':
        homework.delete()
    return redirect('homework_list')

# --- Students ---
from .models import Student, Teacher, ClassSchedule, Attendance

@login_required(login_url='/login/')
def student_list(request):
    students = Student.objects.all().order_by('-joined_date')
    return render(request, 'student_list.html', {'students': students})

@login_required(login_url='/login/')
def student_create(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('parent_phone_number')
        Student.objects.create(
            name=request.POST.get('name'),
            email=email if email else None,
            parent_phone_number=phone if phone else None,
            roll_number=request.POST.get('roll_number'),
            grade_level=request.POST.get('grade_level')
        )
        return redirect('student_list')
    return render(request, 'student_form.html', {'action_title': 'Add'})

import csv
import io
from django.contrib import messages

@login_required(login_url='/login/')
def student_upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file or not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid CSV file.')
            return redirect('student_upload_csv')
            
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string, None) # Skip header
        
        count = 0
        for row in csv.reader(io_string, delimiter=',', quotechar='"'):
            if len(row) >= 5:
                name = row[0].strip()
                email = row[1].strip()
                phone = row[2].strip()
                roll = row[3].strip()
                grade = row[4].strip()
                if name and roll and grade:
                    Student.objects.create(
                        name=name,
                        email=email if email else None,
                        parent_phone_number=phone if phone else None,
                        roll_number=roll,
                        grade_level=grade
                    )
                    count += 1
        messages.success(request, f'{count} students imported successfully!')
        return redirect('student_list')
        
    return render(request, 'student_upload_csv.html')

@login_required(login_url='/login/')
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
    return redirect('student_list')

@login_required(login_url='/login/')
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('parent_phone_number')
        student.name = request.POST.get('name')
        student.email = email if email else None
        student.parent_phone_number = phone if phone else None
        student.roll_number = request.POST.get('roll_number')
        student.grade_level = request.POST.get('grade_level')
        student.save()
        return redirect('student_list')
    return render(request, 'student_form.html', {'action_title': 'Edit', 'student': student})

# --- Teachers ---
@login_required(login_url='/login/')
def teacher_list(request):
    assigned_class = request.GET.get('assigned_class')
    if assigned_class and assigned_class != 'All':
        teachers = Teacher.objects.filter(assigned_class=assigned_class).order_by('-joined_date')
    else:
        teachers = Teacher.objects.all().order_by('-joined_date')
    class_choices = ['Jr KG', 'Sr KG', 'Class 1', 'Class 2', 'Class 3', 'Class 4', 'All Classes']
    return render(request, 'teacher_list.html', {'teachers': teachers, 'selected_class': assigned_class, 'class_choices': class_choices})

@login_required(login_url='/login/')
def teacher_create(request):
    class_choices = ['Jr KG', 'Sr KG', 'Class 1', 'Class 2', 'Class 3', 'Class 4', 'All Classes']
    if request.method == 'POST':
        Teacher.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject_specialty=request.POST.get('subject_specialty'),
            assigned_class=request.POST.get('assigned_class', 'Class 1')
        )
        return redirect('teacher_list')
    return render(request, 'teacher_form.html', {'action_title': 'Add', 'class_choices': class_choices})

@login_required(login_url='/login/')
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    class_choices = ['Jr KG', 'Sr KG', 'Class 1', 'Class 2', 'Class 3', 'Class 4', 'All Classes']
    if request.method == 'POST':
        teacher.name = request.POST.get('name')
        teacher.email = request.POST.get('email')
        teacher.subject_specialty = request.POST.get('subject_specialty')
        teacher.assigned_class = request.POST.get('assigned_class', teacher.assigned_class)
        teacher.save()
        return redirect('teacher_list')
    return render(request, 'teacher_form.html', {'action_title': 'Edit', 'teacher': teacher, 'class_choices': class_choices})

@login_required(login_url='/login/')
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
    return redirect('teacher_list')

# --- Attendance ---
@login_required(login_url='/login/')
def attendance_list(request):
    attendance = Attendance.objects.all().select_related('student').order_by('-date')
    return render(request, 'attendance_list.html', {'attendance': attendance})

@login_required(login_url='/login/')
def attendance_create(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        date = request.POST.get('date')
        status = request.POST.get('status')
        student = get_object_or_404(Student, pk=student_id)
        Attendance.objects.create(student=student, date=date, status=status)
        return redirect('attendance_list')
    students = Student.objects.all()
    return render(request, 'attendance_form.html', {'action_title': 'Add', 'students': students})

# --- Class Schedules ---
@login_required(login_url='/login/')
def schedule_list(request):
    schedules = ClassSchedule.objects.all().select_related('teacher').order_by('day_of_week', 'start_time')
    return render(request, 'schedule_list.html', {'schedules': schedules})

@login_required(login_url='/login/')
def schedule_create(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        teacher = get_object_or_404(Teacher, pk=teacher_id)
        ClassSchedule.objects.create(
            teacher=teacher,
            subject=request.POST.get('subject'),
            day_of_week=request.POST.get('day_of_week'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time')
        )
        return redirect('schedule_list')
    teachers = Teacher.objects.all()
    return render(request, 'schedule_form.html', {'action_title': 'Add', 'teachers': teachers})

# --- Event Photos ---
from .models import EventPhoto

@login_required(login_url='/login/')
def event_photo_list(request):
    photos = EventPhoto.objects.all().order_by('-uploaded_at')
    return render(request, 'event_photo_list.html', {'photos': photos})

@login_required(login_url='/login/')
def event_photo_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        photo = request.FILES.get('photo')
        if photo:
            EventPhoto.objects.create(title=title, photo=photo)
        return redirect('event_photo_list')
    return render(request, 'event_photo_form.html', {'action_title': 'Add'})

# --- Lessons ---
@login_required(login_url='/login/')
def lesson_list(request):
    lessons = Lesson.objects.all().order_by('subject', 'grade_level', 'created_at')
    return render(request, 'lesson_list.html', {'lessons': lessons})

@login_required(login_url='/login/')
def lesson_create(request):
    grade_levels = ['Jr KG', 'Sr KG', 'Class 1', 'Class 2', 'Class 3', 'Class 4']
    if request.method == 'POST':
        Lesson.objects.create(
            subject=request.POST.get('subject'),
            grade_level=request.POST.get('grade_level'),
            title_mr=request.POST.get('title_mr'),
            title_en=request.POST.get('title_en'),
            description_mr=request.POST.get('description_mr'),
            description_en=request.POST.get('description_en'),
            content_mr=request.POST.get('content_mr'),
            content_en=request.POST.get('content_en'),
            icon_res=request.POST.get('icon_res'),
            color_hex=request.POST.get('color_hex')
        )
        return redirect('lesson_list')
    subjects = ['Marathi', 'English', 'Mathematics', 'Rhymes', 'Stories', 'Videos']
    return render(request, 'lesson_form.html', {'action_title': 'Add', 'subjects': subjects, 'grade_levels': grade_levels})

@login_required(login_url='/login/')
def lesson_edit(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    grade_levels = ['Jr KG', 'Sr KG', 'Class 1', 'Class 2', 'Class 3', 'Class 4']
    if request.method == 'POST':
        lesson.subject = request.POST.get('subject')
        lesson.grade_level = request.POST.get('grade_level')
        lesson.title_mr = request.POST.get('title_mr')
        lesson.title_en = request.POST.get('title_en')
        lesson.description_mr = request.POST.get('description_mr')
        lesson.description_en = request.POST.get('description_en')
        lesson.content_mr = request.POST.get('content_mr')
        lesson.content_en = request.POST.get('content_en')
        lesson.icon_res = request.POST.get('icon_res')
        lesson.color_hex = request.POST.get('color_hex')
        lesson.save()
        return redirect('lesson_list')
    subjects = ['Marathi', 'English', 'Mathematics', 'Rhymes', 'Stories', 'Videos']
    return render(request, 'lesson_form.html', {'action_title': 'Edit', 'lesson': lesson, 'subjects': subjects, 'grade_levels': grade_levels})

@login_required(login_url='/login/')
def lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == 'POST':
        lesson.delete()
    return redirect('lesson_list')

# --- Quiz Questions ---
@login_required(login_url='/login/')
def quiz_list(request):
    quizzes = QuizQuestion.objects.all().order_by('subject', 'grade_level', 'created_at')
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

@login_required(login_url='/login/')
def quiz_create(request):
    grade_levels = ['Jr KG', 'Sr KG', 'Class 1', 'Class 2', 'Class 3', 'Class 4']
    if request.method == 'POST':
        QuizQuestion.objects.create(
            subject=request.POST.get('subject'),
            grade_level=request.POST.get('grade_level'),
            question_mr=request.POST.get('question_mr'),
            question_en=request.POST.get('question_en'),
            option_1_en=request.POST.get('option_1_en'),
            option_2_en=request.POST.get('option_2_en'),
            option_3_en=request.POST.get('option_3_en'),
            option_4_en=request.POST.get('option_4_en'),
            option_1_mr=request.POST.get('option_1_mr'),
            option_2_mr=request.POST.get('option_2_mr'),
            option_3_mr=request.POST.get('option_3_mr'),
            option_4_mr=request.POST.get('option_4_mr'),
            correct_answer_index=int(request.POST.get('correct_answer_index')),
            points=int(request.POST.get('points', 10))
        )
        return redirect('quiz_list')
    subjects = ['Marathi', 'English', 'Mathematics']
    return render(request, 'quiz_form.html', {'action_title': 'Add', 'subjects': subjects, 'grade_levels': grade_levels})

@login_required(login_url='/login/')
def quiz_edit(request, pk):
    quiz = get_object_or_404(QuizQuestion, pk=pk)
    grade_levels = ['Jr KG', 'Sr KG', 'Class 1', 'Class 2', 'Class 3', 'Class 4']
    if request.method == 'POST':
        quiz.subject = request.POST.get('subject')
        quiz.grade_level = request.POST.get('grade_level')
        quiz.question_mr = request.POST.get('question_mr')
        quiz.question_en = request.POST.get('question_en')
        quiz.option_1_en = request.POST.get('option_1_en')
        quiz.option_2_en = request.POST.get('option_2_en')
        quiz.option_3_en = request.POST.get('option_3_en')
        quiz.option_4_en = request.POST.get('option_4_en')
        quiz.option_1_mr = request.POST.get('option_1_mr')
        quiz.option_2_mr = request.POST.get('option_2_mr')
        quiz.option_3_mr = request.POST.get('option_3_mr')
        quiz.option_4_mr = request.POST.get('option_4_mr')
        quiz.correct_answer_index = int(request.POST.get('correct_answer_index'))
        quiz.points = int(request.POST.get('points', 10))
        quiz.save()
        return redirect('quiz_list')
    subjects = ['Marathi', 'English', 'Mathematics']
    return render(request, 'quiz_form.html', {'action_title': 'Edit', 'quiz': quiz, 'subjects': subjects, 'grade_levels': grade_levels})

@login_required(login_url='/login/')
def quiz_delete(request, pk):
    quiz = get_object_or_404(QuizQuestion, pk=pk)
    if request.method == 'POST':
        quiz.delete()
    return redirect('quiz_list')

# --- School Notices ---
@login_required(login_url='/login/')
def notice_list(request):
    notices = SchoolNotice.objects.all().order_by('-date')
    return render(request, 'notice_list.html', {'notices': notices})

@login_required(login_url='/login/')
def notice_create(request):
    if request.method == 'POST':
        SchoolNotice.objects.create(
            title_mr=request.POST.get('title_mr'),
            title_en=request.POST.get('title_en'),
            content_mr=request.POST.get('content_mr'),
            content_en=request.POST.get('content_en'),
            author_name=request.POST.get('author_name'),
            is_urgent=request.POST.get('is_urgent') == 'on'
        )
        return redirect('notice_list')
    return render(request, 'notice_form.html', {'action_title': 'Add'})

@login_required(login_url='/login/')
def notice_delete(request, pk):
    notice = get_object_or_404(SchoolNotice, pk=pk)
    if request.method == 'POST':
        notice.delete()
    return redirect('notice_list')

# --- Calendar Events ---
@login_required(login_url='/login/')
def event_list(request):
    events = CalendarEvent.objects.all().order_by('-date')
    return render(request, 'event_list.html', {'events': events})

@login_required(login_url='/login/')
def event_create(request):
    if request.method == 'POST':
        CalendarEvent.objects.create(
            title_mr=request.POST.get('title_mr'),
            title_en=request.POST.get('title_en'),
            date=request.POST.get('date'),
            time=request.POST.get('time'),
            description_mr=request.POST.get('description_mr'),
            description_en=request.POST.get('description_en'),
            color_hex=request.POST.get('color_hex', '#3B82F6')
        )
        return redirect('event_list')
    return render(request, 'event_form.html', {'action_title': 'Add'})

@login_required(login_url='/login/')
def event_delete(request, pk):
    event = get_object_or_404(CalendarEvent, pk=pk)
    if request.method == 'POST':
        event.delete()
    return redirect('event_list')


