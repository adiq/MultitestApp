# -*- encoding: utf8 -*-
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from multitest.models import Test, Question, Answer


def create_actions(request, *args, **kwargs):
    """ Handling "create" / "delete" POST requests
    """

    resolver = {
        'admin:index': Test,
        'admin:test': Question,
        'admin:question': Answer
    }

    if request.method == 'POST':
        target = resolver.get(request.resolver_match.view_name)

        if request.POST.get('delete'):
            to_delete = get_object_or_404(target, pk=request.POST.get('delete'))
            to_delete.delete()

        if request.POST.get('new'):
            new = target.objects.create(**kwargs)
            new.save()


@staff_member_required
def index(request):
    create_actions(request, title='Nowy test.')

    tests = Test.objects.all().order_by('created_at')
    return render(request, 'multitest_admin/index.html', {
        'tests': tests,
    })


@staff_member_required
def test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)

    create_actions(request, test_id, question='Nowe pytanie.', test=test)

    return render(request, 'multitest_admin/test.html', {
        'test': test,
    })


@staff_member_required
def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    create_actions(request, question_id, answer='Nowa odpowiedź.', question=question)

    return render(request, 'multitest_admin/question.html', {
        'question': question,
    })