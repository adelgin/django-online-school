from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import inlineformset_factory
from .models import Question, Choice, Quiz
from django_ckeditor_5.widgets import CKEditor5Widget

from onlineschoolapp.models import Lecture, Question, Quiz, User, Student, Mentor, Teacher, Course, Lesson


class StudentSignUpForm(UserCreationForm):
    """ Форма регистрации для студента. """

    name = forms.CharField(min_length=10, max_length=100, label='Имя и фамилия')
    email = forms.EmailField(min_length=5, max_length=100, label='Электронная почта')
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Курс(-ы), на котором(-ых) будете обучаться:'
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user,
                                         name=self.cleaned_data.get('name'),
                                         email=self.cleaned_data.get('email'))
        student.course_set.add(*self.cleaned_data.get('courses'))
        return user


class MentorSignUpForm(UserCreationForm):
    """ Форма регистрации для ментора. """

    name = forms.CharField(min_length=10, max_length=100, label='Имя и фамилия')
    email = forms.EmailField(min_length=5, max_length=100, label='Электронная почта')
    education = forms.CharField(max_length=100, label='Образование')
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Курс(-ы), на котором(-ых) будете наставником:'
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_mentor = True
        user.save()
        mentor = Mentor.objects.create(user=user, name=self.cleaned_data.get('name'),
                                       email=self.cleaned_data.get('email'),
                                       education=self.cleaned_data.get('education'))
        mentor.course_set.add(*self.cleaned_data.get('courses'))
        return user


class TeacherSignUpForm(UserCreationForm):
    """ Форма регистрации для преподавателя. """

    name = forms.CharField(min_length=10, max_length=100, label='Имя и фамилия')
    email = forms.EmailField(min_length=5, max_length=100, label='Электронная почта')
    education = forms.CharField(max_length=100, label='Образование')
    company = forms.CharField(max_length=100, label='Компания')
    experience = forms.IntegerField(label='Опыт в годах')
    role = forms.ChoiceField(choices=[('Семинарист', 'Семинарист'), ('Лектор', 'Лектор')], label='Роль')
    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all(),
                                             widget=forms.CheckboxSelectMultiple,
                                             required=False,
                                             label='Курс(-ы), на котором(-ых) будете преподавать:')

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user, name=self.cleaned_data.get('name'),
                                         email=self.cleaned_data.get('email'),
                                         education=self.cleaned_data.get('education'),
                                         company=self.cleaned_data.get('company'),
                                         experience=self.cleaned_data.get('experience'),
                                         role=self.cleaned_data.get('role'))
        teacher.course_set.add(*self.cleaned_data.get('courses'))
        return user
    
class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'content', 'image', 'course']
        widgets = {
            'content': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
                config_name="extends"
            )
        }
    
# class LectureForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['content'].widget = CKEditor5Widget(
#             config_name='extends',
#             attrs={'class': 'django_ckeditor_5'}
#         )

#     class Meta:
#         model = Lecture
#         fields = '__all__'

class QuizForm(forms.ModelForm):
    """ Форма для создания теста. """
    class Meta:
        model = Quiz
        fields = ['title', 'lecture']
        widgets = {
            'lecture': forms.Select(attrs={'class': 'form-control'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'type', 'order', 'correct_text_answer']
    
    def __init__(self, *args, **kwargs):
        self.quiz = kwargs.pop('quiz', None)
        super().__init__(*args, **kwargs)

ChoiceFormSet = inlineformset_factory(
    Question, Choice, 
    fields=('text', 'is_correct'), 
    extra=2, 
    can_delete=True
)

class ChoiceForm(forms.ModelForm):
    """ Форма для вариантов ответа """
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Формсет для вариантов ответа
ChoiceFormSet = inlineformset_factory(
    Question, Choice, form=ChoiceForm,
    extra=2, can_delete=True, min_num=1, validate_min=True
)

class MatchingForm(forms.Form):
    """ Форма для создания соответствий """
    left = forms.CharField(label='Левая часть')
    right = forms.CharField(label='Правая часть')