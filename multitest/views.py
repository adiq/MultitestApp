# -*- encoding: utf8 -*-
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from forms import RegisterForm, LoginForm
from models import Test, Answer
from django.core.mail import send_mail


def index(request):
    tests = Test.objects.all().order_by('-created_at')
    return render(request, 'multitest/index.html', {
        'tests': tests,
    })


@login_required(login_url='login')
def test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)

    if request.method == 'POST':
        points = 0
        question_list = test.question_set.all()
        max_points = question_list.count()

        question_id_list = question_list.values_list('id', flat=True)

        correct_answers = []
        user_answers = []
        for q in question_id_list:
            correct_answers += (list(Answer.objects.filter(question=q, is_correct=True).values_list('id', flat=True)),)
            user_answers += (request.POST.getlist('question%s[]' % q),)
        user_answers = arr_to_int(user_answers)

        for a in user_answers:
            if a in correct_answers:
                points += 1

        if request.POST.get('sendMail'):
            send_mail('Twoje wyniki testu %s' % test.title,
                      u'Witaj %s. W teście "%s" odpowiedziałeś prawidłowo na %d z %d pytań. Gratulacje.' %
                      (request.user.username, test.title, points, max_points),
                      'tshmultitest@o2.pl',
                      [request.user.email], fail_silently=True)

        return render(request, 'multitest/result.html', {
            'test': test,
            'points': points,
            'max_points': max_points,
        })

    else:
        return render(request, 'multitest/test.html', {
            'test': test,
        })


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = auth.authenticate(username=data['login'], password=data['password'])
            if user and user.is_active:
                auth.login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Niepoprawne dane!')
                return redirect('login')

    if request.GET.get('next'):
        messages.warning(request, 'Wymagane logowanie!')
    form = LoginForm()

    return render(request, 'multitest/login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if not data['verify'].lower() == "warszawa":
                messages.warning(request, u'Na pewno taka jest stolica Polski?')
                return redirect('register')
            try:
                user = User.objects.create_user(username=unicode(data['login']), password=unicode(data['password']),
                                                email=unicode(data['email']))
            except:
                messages.warning(request, u'Wystąpił błąd lub taki użytkownik już istnieje!')
                return redirect('register')

            user.is_active = True
            user.is_staff = False
            user.save()

            messages.success(request, 'Konto utworzone! ;)')
            return redirect('login')

    form = RegisterForm()
    return render(request, 'multitest/register.html', {'form': form})


def arr_to_int(arr):
    """ Helper to convert strings lists (and string lists in lists) to int.
    """
    new_arr = []
    for item in arr:
        if isinstance(item, list):
            new_arr.append(arr_to_int(item))
        else:
            new_arr.append(int(item))
    return new_arr