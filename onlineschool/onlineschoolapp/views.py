from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .models import Quiz, Student, StudentAnswer, Choice
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Avg
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView
from onlineschoolapp.forms import LectureForm, QuestionForm, QuizForm, StudentSignUpForm, TeacherSignUpForm, MentorSignUpForm
from onlineschoolapp.models import Lecture, Question, Quiz, calc_online_school_stats
from onlineschoolapp.models import User, Course, Teacher, Student, Mentor, Lesson, Grade
from onlineschoolapp.filters import CourseFilter, TeacherFilter, StudentFilter, MentorFilter, LessonFilter
from onlineschoolapp.decorators import teacher_required, student_required, mentor_required

from django.forms import formset_factory
from django.http import Http404, JsonResponse
from .models import Question, Choice, StudentAnswer
from .forms import QuestionForm, ChoiceForm, ChoiceFormSet, MatchingForm


class CourseListView(generic.ListView):
    """ Отображение информации о курсах. """

    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CourseFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CourseDetailView(generic.DetailView):
    """ Отображение детальной информации о курсе. """
    model = Course


class TeacherListView(generic.ListView):
    """ Отображение информации о преподавателях. """
    model = Teacher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TeacherFilter(self.request.GET, queryset=self.get_queryset())
        return context


class TeacherDetailView(generic.DetailView):
    """ Отображение детальной информации о преподавателе. """
    model = Teacher


class StudentListView(LoginRequiredMixin, generic.ListView):
    """ Отображение информации о студентах. """

    model = Student
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = StudentFilter(self.request.GET, queryset=self.get_queryset())
        return context


class StudentDetailView(generic.DetailView):
    """ Отображение детальной информации о студенте. """
    model = Student


class MentorListView(LoginRequiredMixin, generic.ListView):
    """ Отображение информации о менторах. """

    model = Mentor
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = MentorFilter(self.request.GET, queryset=self.get_queryset())
        return context


class MentorDetailView(generic.DetailView):
    """ Отображение детальной информации о менторе. """
    model = Mentor


class LessonListView(LoginRequiredMixin, generic.ListView):
    """ Отображение информации об уроках. """

    model = Lesson
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = LessonFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        if self.request.user.is_student:
            return Lesson.objects.filter(course_id__student__user=self.request.user)
        else:
            return Lesson.objects.all()


class LessonDetailView(generic.DetailView):
    """ Отображение с детальной информацией об уроке. """
    model = Lesson


class SignUpView(TemplateView):
    """ Отображение для регистрации. """
    template_name = 'registration/signup.html'


class StudentSignUpView(CreateView):
    """ Отображение для регистрации студента. """

    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return index(self.request)


class TeacherSignUpView(CreateView):
    """ Отображение для регистрации преподавателя. """

    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return index(self.request)


class MentorSignUpView(CreateView):
    """ Отображение для регистрации ментора. """

    model = User
    form_class = MentorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'mentor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return index(self.request)


@method_decorator([login_required, student_required], name='dispatch')
class StudentGradesListView(LoginRequiredMixin, generic.ListView):
    """ Отображение оценок студента. """

    model = Student
    template_name ='onlineschoolapp/student_grades_list.html'

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)
    

class StudentLecturesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Lecture
    template_name = 'onlineschoolapp/student_lectures.html'
    context_object_name = 'lectures'

    def test_func(self):
        return self.request.user.is_student

    def get_queryset(self):
        # Получаем лекции только для курсов, на которые записан студент
        student = self.request.user.student
        return Lecture.objects.filter(
            course__in=student.course_set.all()
        ).order_by('-created_at')


@method_decorator([login_required, teacher_required], name='dispatch')
class LessonCreate(CreateView):
    """ Отображение для создания урока. """

    model = Lesson
    fields = ['title', 'course_id', 'teacher_id', 'link']
    success_url = reverse_lazy('lessons')


@method_decorator([login_required, teacher_required], name='dispatch')
class LessonDelete(DeleteView):
    """ Отображение для удаления урока. """

    model = Lesson
    success_url = reverse_lazy('lessons')


@method_decorator([login_required, teacher_required], name='dispatch')
class GradeUpdate(UpdateView):
    """ Отображение для изменения урока. """

    model = Grade
    fields = ['course', 'student', 'homework1', 'homework2', 'project', 'final_mark']
    success_url = reverse_lazy('students')


@method_decorator([login_required, teacher_required], name='dispatch')
class LectureCreate(CreateView):
    model = Lecture
    form_class = LectureForm
    template_name = 'onlineschoolapp/lecture_form.html'

    def form_valid(self, form):
        # Устанавливаем преподавателя (текущего пользователя)
        form.instance.teacher = self.request.user.teacher
        # Сохраняем лекцию и получаем объект
        self.object = form.save()
        # Перенаправляем на страницу просмотра лекции
        return super().form_valid(form)

    def get_success_url(self):
        # Возвращаем URL для просмотра только что созданной лекции
        return reverse('lecture_detail', kwargs={'pk': self.object.pk})
        

@method_decorator([login_required, teacher_required], name='dispatch')
class QuizCreate(LoginRequiredMixin, generic.CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'onlineschoolapp/quiz_form.html'

    def form_valid(self, form):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        form.instance.teacher = teacher
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('quiz_detail', args=[self.object.id])

@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionCreate(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'onlineschoolapp/question_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['quiz'] = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['choice_formset'] = ChoiceFormSet(self.request.POST)
        else:
            context['choice_formset'] = ChoiceFormSet(queryset=Choice.objects.none())
        return context

    def form_valid(self, form):
        quiz = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        form.instance.quiz = quiz
        
        # Сохраняем вопрос, но не коммитим в БД пока
        self.object = form.save(commit=False)
        
        if form.instance.type == 'text':
            if not form.cleaned_data.get('correct_text_answer'):
                form.add_error('correct_text_answer', 'Укажите правильный ответ')
                return self.form_invalid(form)
        
        elif form.instance.type in ['single_choice', 'multiple_choice']:
            choice_formset = ChoiceFormSet(self.request.POST, instance=self.object)
            if not choice_formset.is_valid():
                return self.form_invalid(form)
                
            # Проверяем, что есть хотя бы один правильный вариант
            if not any(choice_form.cleaned_data.get('is_correct') 
                    for choice_form in choice_formset if choice_form.cleaned_data):
                form.add_error(None, 'Укажите хотя бы один правильный вариант')
                return self.form_invalid(form)
        
        elif form.instance.type == 'matching':
            pairs = []
            for i in range(len(self.request.POST.getlist('matching_left[]'))):
                left = self.request.POST.getlist('matching_left[]')[i]
                right = self.request.POST.getlist('matching_right[]')[i]
                if left and right:
                    pairs.append({'left': left, 'right': right})
            
            if len(pairs) < 2:
                form.add_error(None, 'Нужно минимум 2 пары для соответствия')
                return self.form_invalid(form)
                
            form.instance.matching_pairs = pairs
        
        # Сохраняем вопрос
        self.object.save()
        
        # Сохраняем варианты ответов для вопросов с выбором
        if form.instance.type in ['single_choice', 'multiple_choice']:
            choice_formset.instance = self.object
            choice_formset.save()
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('quiz_detail', kwargs={'pk': self.kwargs['pk']})



    # def get_success_url(self):
    #     return reverse('quiz_detail', args=[self.kwargs['quiz_id']])

@method_decorator([login_required, teacher_required], name='dispatch')
class QuizDetailView(LoginRequiredMixin, generic.DetailView):
    model = Quiz
    template_name = 'onlineschoolapp/quiz_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = self.object.questions.all().order_by('order')
        return context

@method_decorator([login_required, student_required], name='dispatch')
class TakeQuizView(LoginRequiredMixin, generic.DetailView):
    model = Quiz
    template_name = 'onlineschoolapp/take_quiz.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.object
        student = self.request.user.student
        
        questions_data = []
        for question in quiz.questions.all().order_by('order'):
            student_answer = StudentAnswer.objects.filter(
                student=student,
                question=question
            ).first()
            
            selected_ids = []
            if student_answer:
                selected_ids = list(student_answer.selected_choices.values_list('id', flat=True))
            
            form = self.create_question_form(question, selected_ids)
            
            questions_data.append({
                'question': question,
                'form': form,
                'answered': student_answer is not None,
                'is_correct': student_answer.is_correct if student_answer else False,
                'selected_ids': selected_ids
            })
        
        context['questions'] = questions_data
        return context
    
    def create_question_form(self, question, selected_ids):
        if question.type == 'single_choice':
            form = forms.Form()
            form.fields['answer'] = forms.ModelChoiceField(
                queryset=question.choices.all(),
                widget=forms.RadioSelect,
                initial=selected_ids[0] if selected_ids else None,
                required=False
            )
        elif question.type == 'multiple_choice':
            form = forms.Form()
            form.fields['answers'] = forms.ModelMultipleChoiceField(
                queryset=question.choices.all(),
                widget=forms.CheckboxSelectMultiple,
                initial=selected_ids,
                required=False
            )
        else:
            form = forms.Form()
            form.fields['answer'] = forms.CharField(
                widget=forms.Textarea(attrs={'rows': 2}),
                required=False
            )
        return form

@method_decorator([login_required, student_required], name='dispatch')
class SubmitQuizView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        quiz = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        student = request.user.student
        
        for question in quiz.questions.all():
            answer_key = f'question_{question.id}'
            
            if question.type == 'text':
                self.process_text_answer(request, question, student, answer_key)
            elif question.type == 'single_choice':
                self.process_single_choice(request, question, student, answer_key)
            elif question.type == 'multiple_choice':
                self.process_multiple_choice(request, question, student, answer_key)
        
        return redirect('quiz_results', pk=quiz.id)
    
    def process_single_choice(self, request, question, student, answer_key):
        choice_id = request.POST.get(answer_key)
        if not choice_id:
            return
            
        selected_choice = get_object_or_404(Choice, pk=choice_id)
        
        student_answer, created = StudentAnswer.objects.update_or_create(
            student=student,
            question=question,
            defaults={
                'is_correct': selected_choice.is_correct
            }
        )
        student_answer.selected_choices.clear()
        student_answer.selected_choices.add(selected_choice)
    
    def process_multiple_choice(self, request, question, student, answer_key):
        choice_ids = request.POST.getlist(answer_key)
        selected_choices = Choice.objects.filter(pk__in=choice_ids)
        correct_choices = question.choices.filter(is_correct=True)
        
        is_correct = (
            set(selected_choices.values_list('id', flat=True)) == 
            set(correct_choices.values_list('id', flat=True))
        )
        
        student_answer, created = StudentAnswer.objects.update_or_create(
            student=student,
            question=question,
            defaults={
                'is_correct': is_correct
            }
        )
        student_answer.selected_choices.set(selected_choices)
    
    def process_text_answer(self, request, question, student, answer_key):
        text_answer = request.POST.get(answer_key, '').strip()
        is_correct = text_answer.lower() == question.correct_text_answer.lower()
        
        StudentAnswer.objects.update_or_create(
            student=student,
            question=question,
            defaults={
                'text_answer': text_answer,
                'is_correct': is_correct
            }
        )
    
class QuizResultsView(LoginRequiredMixin, generic.DetailView):
    model = Quiz
    template_name = 'onlineschoolapp/quiz_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.object
        
        if hasattr(self.request.user, 'teacher'):
            # Режим преподавателя - просмотр всех студентов
            teacher = self.request.user.teacher
            
            # Проверяем, принадлежит ли тест преподавателю
            if quiz.teacher != teacher:
                raise PermissionDenied("Это не ваш тест")
            
            # Получаем всех студентов, проходивших тест
            student_answers = StudentAnswer.objects.filter(
                question__quiz=quiz
            ).select_related('student', 'question')
            
            # Группируем результаты по студентам
            students_results = {}
            for answer in student_answers:
                if answer.student not in students_results:
                    students_results[answer.student] = {
                        'answers': [],
                        'correct_count': 0,
                        'total_questions': 0
                    }
                students_results[answer.student]['answers'].append(answer)
                if answer.is_correct:
                    students_results[answer.student]['correct_count'] += 1
                students_results[answer.student]['total_questions'] = quiz.questions.count()
            
            context['teacher_mode'] = True
            context['students_results'] = students_results
            
        elif hasattr(self.request.user, 'student'):
            # Режим студента - просмотр своих результатов
            student = self.request.user.student
            answers = StudentAnswer.objects.filter(
                student=student,
                question__quiz=quiz
            )
            
            correct_answers = answers.filter(is_correct=True).count()
            total_questions = quiz.questions.count()
            
            context['teacher_mode'] = False
            context['questions'] = [
                {
                    'question': answer.question,
                    'student_answer': answer,
                    'is_correct': answer.is_correct
                } 
                for answer in answers
            ]
            context['correct_answers'] = correct_answers
            context['total_questions'] = total_questions
            context['percentage'] = round((correct_answers / total_questions) * 100) if total_questions else 0
            
        else:
            raise PermissionDenied("Доступ запрещен")
            
        return context
    
class LectureDetailView(DetailView):
    model = Lecture
    template_name = 'onlineschoolapp/lecture_detail.html'
    context_object_name = 'lecture'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем связанные тесты
        context['quizzes'] = self.object.quizzes.all()
        return context

class LectureUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Lecture
    form_class = LectureForm
    template_name = 'onlineschoolapp/lecture_form.html'
    
    def test_func(self):
        lecture = self.get_object()
        return self.request.user.is_teacher and lecture.teacher.user == self.request.user
    
    def get_success_url(self):
        return reverse('lecture_detail', kwargs={'pk': self.object.id})
    
@method_decorator([login_required, teacher_required], name='dispatch')
class TeacherLecturesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Lecture
    template_name = 'onlineschoolapp/teacher_lectures.html'
    context_object_name = 'lectures'

    def test_func(self):
        return self.request.user.is_teacher

    def get_queryset(self):
        # Получаем только лекции текущего преподавателя
        teacher = self.request.user.teacher
        return Lecture.objects.filter(
            teacher=teacher
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.request.user.teacher
        
        # Добавляем статистику по лекциям
        lectures = self.get_queryset()
        context['total_lectures'] = lectures.count()
        context['recent_lectures'] = lectures[:5]  # Последние 5 лекций
        
        return context

@method_decorator([login_required, teacher_required], name='dispatch')
class LectureDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Lecture
    template_name = 'onlineschoolapp/lecture_confirm_delete.html'
    
    def test_func(self):
        lecture = self.get_object()
        return lecture.teacher.user == self.request.user
    
    def get_success_url(self):
        return reverse('teacher_lectures')
    
class StudentQuizDetailsView(LoginRequiredMixin, generic.DetailView):
    model = Quiz
    template_name = 'onlineschoolapp/student_quiz_details.html'
    pk_url_kwarg = 'quiz_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.object
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        
        if not hasattr(self.request.user, 'teacher') or quiz.teacher != self.request.user.teacher:
            raise PermissionDenied("Доступ запрещен")
        
        answers = StudentAnswer.objects.filter(
            student=student,
            question__quiz=quiz
        ).select_related('question')
        
        context['student'] = student
        context['answers'] = answers
        context['correct_count'] = answers.filter(is_correct=True).count()
        context['total_questions'] = quiz.questions.count()
        
        return context
    


def index(request):
    num_courses = Course.objects.count()
    num_teachers = Teacher.objects.count()
    num_students = Student.objects.count()
    
    # Получаем последние 5 лекций
    latest_lectures = Lecture.objects.all().order_by('-created_at')[:5]
    
    # Получаем доступные тесты
    available_quizzes = Quiz.objects.all()
    completed_quizzes = []
    
    if request.user.is_authenticated and request.user.is_student:
        student = Student.objects.get(user=request.user)
        completed_quizzes = Quiz.objects.filter(
            questions__studentanswer__student=student
        ).distinct()
    
    context = {
        'num_courses': num_courses,
        'num_teachers': num_teachers,
        'num_students': num_students,
        'latest_lectures': latest_lectures,
        'available_quizzes': available_quizzes,
        'completed_quizzes': completed_quizzes,
    }
    
    return render(request, 'index.html', context=context)