from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """
    Модель для пользователя.
    Пользователь может принадлежать к одной из трех групп: студент, преподаватель, ментор.
    """
    is_student = models.BooleanField(default=False, verbose_name='Студент')
    is_teacher = models.BooleanField(default=False, verbose_name='Преподаватель')
    is_mentor = models.BooleanField(default=False, verbose_name='Ментор')


class Teacher(models.Model):
    """ Модель для преподавателя. """

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, verbose_name='Имя и фамилия преподавателя')
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name='E-mail преподавателя')
    role = models.CharField(max_length=20, blank=True, null=True, verbose_name='Роль преподавателя',
                            choices=[('Семинарист', 'Семинарист'), ('Лектор', 'Лектор')])
    education = models.CharField(max_length=100, blank=True, null=True, verbose_name='Образование преподавателя (ВУЗ)')
    company = models.CharField(max_length=100, blank=True, null=True, verbose_name='Компания')
    experience = models.SmallIntegerField(blank=True, null=True, verbose_name='Опыт в годах')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('teacher_detail', args=[str(self.id)])

    class Meta:
        ordering = ['name']


class Student(models.Model):
    """ Модель для студента. """

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, verbose_name='Имя студента')
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name='E-mail студента')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('student_detail', args=[str(self.id)])

    class Meta:
        ordering = ['name']


class Mentor(models.Model):
    """ Модель для ментора. """

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=False, verbose_name='Имя ментора')
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name='E-mail ментора')
    education = models.CharField(max_length=100, blank=True, null=True, verbose_name='Образование ментора (ВУЗ)')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mentor_detail', args=[str(self.id)])

    class Meta:
        ordering = ['name']


class Course(models.Model):
    """ Модель для курса. """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, verbose_name='Название курса')
    description = models.TextField(blank=False, verbose_name='Описание курса')
    duration = models.PositiveSmallIntegerField(blank=False, default=6, verbose_name='Продолжительность курса',
                                                choices=[(6, '6 месяцев'), (12, '12 месяцев'), (18, '18 месяцев')])
    price = models.PositiveIntegerField(blank=False, default=50000, verbose_name='Стоимость курса')
    student = models.ManyToManyField(Student, through='Grade')
    teacher = models.ManyToManyField(Teacher)
    mentor = models.ManyToManyField(Mentor)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('course_detail', args=[str(self.id)])

    class Meta:
        ordering = ['id']


class Lesson(models.Model):
    """ Модель для урока. """

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=40, blank=False, verbose_name='Тема занятия')
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    teacher_id = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True,
                                   verbose_name='Преподаватель')
    link = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ссылка на занятие в Zoom')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson_detail', args=[str(self.id)])

    class Meta:
        ordering = ['course_id']


class Grade(models.Model):
    """ Модель для оценок. """

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    homework1 = models.SmallIntegerField(blank=True, null=True, verbose_name='Оценка за 1 ДЗ',
                                         choices=[(2, 2), (3, 3), (4, 4), (5, 5)])
    homework2 = models.SmallIntegerField(blank=True, null=True, verbose_name='Оценка за 2 ДЗ',
                                         choices=[(2, 2), (3, 3), (4, 4), (5, 5)])
    project = models.SmallIntegerField(blank=True, null=True, verbose_name='Оценка за проект',
                                       choices=[(2, 2), (3, 3), (4, 4), (5, 5)])
    final_mark = models.FloatField(blank=True, null=True, verbose_name='Оценка за курс')

    class Meta:
        ordering = ['course']

class Lecture(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='lectures/', blank=True, null=True)
    video = models.FileField(upload_to='lectures/videos/', blank=True, null=True,
                           help_text="Загрузите видеофайл")
    audio = models.FileField(upload_to='lectures/audio/', blank=True, null=True,
                           help_text="Загрузите аудиофайл")
    youtube_url = models.URLField(blank=True, null=True,
                                help_text="Или вставьте ссылку на YouTube")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lecture_detail', args=[str(self.id)])
    
    @property
    def quizzes(self):
        return self.quiz_set.all()

class Quiz(models.Model):
    """ Модель для теста. """
    title = models.CharField(max_length=200, verbose_name='Название теста')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='quizzes', verbose_name='Лекция')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Преподаватель')

    def __str__(self):
        return self.title

class Question(models.Model):
    """ Модель для вопросов теста. """
    QUESTION_TYPES = (
        ('text', 'Текстовый ответ'),
        ('single_choice', 'Выбор одного варианта'),
        ('multiple_choice', 'Выбор нескольких вариантов'),
        ('matching', 'Установление соответствия'),
    )
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', verbose_name='Тест')
    text = models.TextField(verbose_name='Текст вопроса')
    type = models.CharField(max_length=20, choices=QUESTION_TYPES, verbose_name='Тип вопроса')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок вопроса')
    
    # Для текстовых вопросов
    correct_text_answer = models.CharField(max_length=200, blank=True, null=True, verbose_name='Правильный текстовый ответ')
    
    # Для вопросов на соответствие (храним как JSON)
    matching_pairs = models.JSONField(blank=True, null=True, verbose_name='Пары для соответствия')
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.text[:50]}... ({self.get_type_display()})"

class Choice(models.Model):
    """ Варианты ответов для вопросов с выбором """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200, verbose_name='Текст варианта')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный вариант')
    
    def __str__(self):
        return self.text

class StudentAnswer(models.Model):
    """ Ответы студентов на вопросы """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text_answer = models.TextField(blank=True, null=True)
    selected_choices = models.ManyToManyField(Choice, blank=True)
    matching_answer = models.JSONField(blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'question')
    
    def __str__(self):
        return f"Ответ {self.student.name} на вопрос {self.question.id}"


def calc_online_school_stats():
    """ Расчёт основных показателей онлайн-школы для вывода на главной странице. """

    num_courses = Course.objects.all().count()
    num_teachers = Teacher.objects.all().count()
    num_students = Student.objects.all().count()
    return num_courses, num_teachers, num_students


def calc_student_final_mark(instance, **kwargs):
    """ Автоматический расчёт итоговой оценки за курс, если выставлены оценки за ДЗ1, ДЗ2 и проект. """

    if instance.homework1 and instance.homework2 and instance.project:
        instance.final_mark = 1 / 3 * sum([instance.homework1, instance.homework2, instance.project])
    return instance.final_mark


pre_save.connect(calc_student_final_mark, sender=Grade, dispatch_uid=__file__)
